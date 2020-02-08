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
# This is the common setup.

set -eo pipefail


check_if_changed(){
    # Ignore this test if there are no changes.
    cd "${KOKORO_ARTIFACTS_DIR}"/github/ai-platform-samples/"${CAIP_TEST_DIR}"
    DIFF=$(git diff master "${KOKORO_GITHUB_PULL_REQUEST_COMMIT}" "${PWD}")
    echo -e "git diff:\n ${DIFF}"
    if [[ -z ${DIFF} ]]; then
        echo -e "Test ignored; directory was not modified in pull request ${KOKORO_GITHUB_PULL_REQUEST_NUMBER}"
        exit 0
    fi

}


project_setup(){
    # Update to latest SDK for gcloud ai-platform command.
    local KEYFILE="${KOKORO_GFILE_DIR}/keyfile.json"
    gcloud components update --quiet
    export GOOGLE_APPLICATION_CREDENTIALS="${KEYFILE}"
    gcloud auth activate-service-account --key-file "${KEYFILE}"
    gcloud config list
}


create_virtualenv(){
    sudo pip install virtualenv
    virtualenv "${KOKORO_ARTIFACTS_DIR}"/envs/venv
    source "${KOKORO_ARTIFACTS_DIR}"/envs/venv/bin/activate
    # Install dependencies.
    pip install --upgrade -r requirements.txt
}


install_and_run_flake8() {
    pip install -q flake8 --user
    # Run Flake in current directory.
    cd "${KOKORO_ARTIFACTS_DIR}"/github/ai-platform-samples/"${CAIP_TEST_DIR}"
    flake8 --max-line-length=80 . --statistics
    result=$?
    if [ ${result} -ne 0 ];then
      echo -e "\n Testing failed: flake8 returned a non-zero exit code. \n"
      exit 1
    else
      echo -e "\n flake8 run successfully in directory $(pwd).\n"
    fi
}

main(){
    cd github/ai-platform-samples/
    check_if_changed
    project_setup
    create_virtualenv
    install_and_run_flake8
    # Run specific test.
    bash "${KOKORO_ARTIFACTS_DIR}"/"${CAIP_TEST_SCRIPT}"

}

main
