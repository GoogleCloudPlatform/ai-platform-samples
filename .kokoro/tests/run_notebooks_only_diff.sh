#!/bin/bash
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# `-e` enables the script to automatically fail when a command fails
# `-o pipefail` sets the exit code to the rightmost comment to exit with a non-zero
set -eo pipefail
# Enables `**` to include files nested inside sub-folders
shopt -s globstar

project_setup(){
    if [[ -z "${PROJECT_ROOT:-}" ]]; then
        PROJECT_ROOT="github/ai-platform-samples"
    fi

    cd "${PROJECT_ROOT}"

    # add user's pip binary path to PATH
    export PATH="${HOME}/.local/bin:${PATH}"

    # On kokoro, we should be able to use the default service account. We
    # need to somehow bootstrap the secrets on other CI systems.
    if [[ "${TRAMPOLINE_CI}" == "kokoro" ]]; then
        # This script will create 3 files:
        # - testing/test-env.sh
        # - testing/service-account.json
        # - testing/client-secrets.json
        ./.kokoro/scripts/decrypt-secrets.sh
    fi

    source ./testing/test-env.sh
    export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/testing/service-account.json

    # For cloud-run session, we activate the service account for gcloud sdk.
    gcloud auth activate-service-account \
           --key-file "${GOOGLE_APPLICATION_CREDENTIALS}"
}

maybe_exit_on_failure () {
    EXIT_STATUS=$?
    if [[ "$EXIT_STATUS" != 0 ]]; then
        exit "$EXIT_STATUS"
    fi
}

install_cloud_packages () {
    # Install AI Platform pre-requisites:
    # https://cloud.google.com/ai-platform/training/docs/runtime-version-list
    echo "Installing Google Cloud Python dependencies..."
    python3 -m pip install -U -q \
        google-api-python-client \
        google-cloud-bigquery \
        google-cloud-bigtable \
        google-cloud-datastore \
        google-cloud-logging \
        google-cloud-pubsub \
        google-cloud-resource-manager \
        google-cloud-storage \
        absl-py \
        astor \
        cloudml-hypertune \
        crcmod \
        future \
        grpcio \
        httplib2 \
        imageio \
        joblib \
        matplotlib \
        mock \
        numpy \
        oauth2client \
        pandas \
        Paste \
        PILLOW \
        pydot \
        python-dateutil \
        python-json-logger \
        PyYAML \
        requests \
        scikit-learn \
        scipy \
        seaborn \
        six \
        sklearn \
        statsmodels \
        sympy \
        tabulate \
        tornado \
        webapp2 \
        WebOb \
        wheel \
        witwidget \
        wrapt \
        xgboost
    maybe_exit_on_failure
}

install_jupyter () {
    echo "Installing Jupyter..."
    python3 -m pip install -U -q \
        ipython \
        jupyter \
        nbconvert
    maybe_exit_on_failure
}

get_date () {
    # Return current date.
    CURRENT_DATE=$(date +%Y%m%d_%H%M%S)
    echo "${CURRENT_DATE}"
}

update_value () {
    # replace variable in notebook in-line. example:
    # "PROJECT_ID = '[your-project-id]' -> "PROJECT_ID = 'gcp-project'
    sed -i -E "s/(\"$1.*\=.*)\[.*\](.*)/\1$2\2/" "$3"
}

update_notebook_install () {
  # remove --user as install already happening inside virtual environment
  PIP_INSTALL_USER='\--user'
  if grep -q "$PIP_INSTALL_USER" "$1"; then
    sed -i 's/--user//g' "$1"
  fi
}

cloud_notebooks_update_contents () {
    # replace variables inside .ipynb files
    # looking for this format inside notebooks:
    # VARIABLE_NAME = '[description]'
    for notebook in $1
    do
        update_value "PROJECT_ID" "${GOOGLE_CLOUD_PROJECT}" "$notebook"
        update_value "REGION" "${REGION}" "$notebook"
        update_value "BUCKET_NAME" "${BUCKET_NAME}" "$notebook"
        update_value "OUTPUT_DIR" "$(_get_date)" "$notebook"
        update_value "USER" "${NOTEBOOKS_USER}" "$notebook"
        # update pip installation settings
        update_notebook_install "$notebook"
    done
}

run_tests() {
    # Switch to 'fail at end' to allow all tests to complete before exiting.
    set +e
    # Use RTN to return a non-zero value if the test fails.
    RTN=0
    ROOT=$(pwd)

    # Only check notebooks modified in this pull request.
    notebooks="$(git diff --name-only master | grep '\.ipynb$' || true)"

    if [[ -n "$notebooks" ]]; then
        cloud_notebooks_update_contents $notebooks
        echo "Running notebooks..."
        jupyter nbconvert \
            --Exporter.preprocessors=[\"./.kokoro/notebooks/preprocess.remove_no_execute_cells\"] \
            --ClearOutputPreprocessor.enabled=True \
            --to notebook \
            --execute $notebooks
    else
        echo "No notebooks modified in this pull request."
    fi

    RTN=$?
    cd "$ROOT"

    # Remove secrets if we used decrypt-secrets.sh.
    if [[ -f "${KOKORO_GFILE_DIR}/secrets_viewer_service_account.json" ]]; then
        rm testing/{test-env.sh,client-secrets.json,service-account.json}
    fi

    exit "$RTN"
}

main(){
    project_setup
    install_cloud_packages
    install_jupyter
    run_tests
}

main
