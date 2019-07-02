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
# Exports variables for project setup.
# set -euxo pipefail


function err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
  return 1
}

function export_variables(){
    # Set variables.
    export RUNTIME_VERSION=1.13
    export PYTHON_VERSION=3.5
    export REGION=us-central1

    # Replace "your-gcp-project-id" with your GCP PROJECT ID
    export PROJECT_ID="endromodal"

    # Replace "your-gcp-bucket-name" with a universally unique name for a GCS bucket (Don't include gs://).
    export BUCKET_NAME="endromodal-dummy"

    # Replace "path/to/service/account/key" with the full path to the
    # service account key file which you created and downloaded.
    export GOOGLE_APPLICATION_CREDENTIALS="/Users/shahins/config/endromodal-sa.json"

    if [[ ${PROJECT_ID} == "your-gcp-project-id" ]]; then
      err "Please set PROJECT_ID to your GCP Project ID"
    fi

    if [[ ${BUCKET_NAME} == "your-gcp-bucket-name" ]]; then
      err "Please set BUCKET_NAME to an existing GCS bucket"
    fi

    if [[ ${GOOGLE_APPLICATION_CREDENTIALS} == "path/to/service/account/key" || -z ${GOOGLE_APPLICATION_CREDENTIALS} ]];
    then
      err "Please set GOOGLE_APPLICATION_CREDENTIALS to the path to your service account key"
    fi
}

main(){
    export_variables || err "Unable to set variables"
}

main "$@"