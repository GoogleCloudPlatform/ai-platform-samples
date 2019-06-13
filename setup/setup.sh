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

#!/bin/bash

export RUNTIME_VERSION=1.13
export PYTHON_VERSION=3.5
export REGION=us-central1

# Replace "your-gcp-project-id" with your gcp PROJECT ID
export PROJECT_ID="your-gcp-project-id"

# Replace "your-gcp-bucket-name" with a universally unique name for a GCS bucket
export BUCKET_NAME="your-gcp-bucket-name"

# Replace "path/to/service/account/key" with the full path to the
# service account key file which you created and downloaded
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service/account/key"


if [[ ${PROJECT_ID} == "your-gcp-project-id" ]]
then
  echo "Warning: Please set PROJECT_ID to your gcp Project ID"
fi

if [[ ${BUCKET_NAME} == "your-gcp-bucket-name" ]]
then
  echo "Warning: Please set BUCKET_NAME to an existing GCS bucket"
fi

if [[ -z ${GOOGLE_APPLICATION_CREDENTIALS} == "path/to/service/account/key" ]]
then
  echo "Warning: Please set GOOGLE_APPLICATION_CREDENTIALS to the path to your service account key"
fi