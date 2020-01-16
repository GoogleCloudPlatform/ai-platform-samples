#!/bin/bash

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

set -v

# This is the common setup.
echo "Submitting an AI Platform job..."

TIER="BASIC" # BASIC | BASIC_GPU | STANDARD_1 | PREMIUM_1

export MODEL_NAME="quickstart" # change to your model name

PACKAGE_PATH=./trainer # this can be a gcs location to a zipped and uploaded package
export MODEL_DIR=gs://${BUCKET_NAME}/${MODEL_NAME}/model

gsutil mb gs://${BUCKET_NAME}

CURRENT_DATE=`date +%Y%m%d_%H%M%S`
JOB_NAME=train_${MODEL_NAME}_${CURRENT_DATE}

gcloud ai-platform jobs submit training ${JOB_NAME} \
        --job-dir=${MODEL_DIR} \
        --runtime-version=${RUNTIME_VERSION} \
        --region=${REGION} \
        --scale-tier=${TIER} \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH}  \
        --python-version=${PYTHON_VERSION} \
        --stream-logs \
        -- \
	    ${MODEL_DIR}

set -

# Notes:
# use --packages instead of --package-path if gcs location
# add --reuse-job-dir to resume training
