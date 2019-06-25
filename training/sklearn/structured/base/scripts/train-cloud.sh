#!/bin/bash
# Copyright 2019 Google LLC. All Rights Reserved.
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
# Runs a training job in AI platform.
set -v

echo "Submitting an AI Platform job..."

TIER="BASIC" # BASIC | BASIC_GPU | STANDARD_1 | PREMIUM_1

export MODEL_NAME="sklearn_taxi"

PACKAGE_PATH=./trainer # this can be a gcs location to a zipped and uploaded package
export MODEL_DIR=gs://${BUCKET_NAME}/${MODEL_NAME}

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
        --input=${GCS_TAXI_TRAIN_BIG} \
        --n-estimators=20 \
        --max-depth=3

# Notes:
# GCS_TAXI_TRAIN_BIG is set by datasets/downlaod-taxi.sh script
# use --packages instead of --package-path if gcs location
# add --reuse-job-dir to resume training
