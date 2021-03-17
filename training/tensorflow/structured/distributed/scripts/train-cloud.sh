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
# Runs a distributed training job in AI platform.
set -v
echo "Submitting an AI Platform job..."

REGION=us-central1
MODEL_NAME="tensorflow_taxi" # change to your model name

PACKAGE_PATH=./trainer # this can be a gcs location to a zipped and uploaded package
MODEL_DIR=gs://${BUCKET_NAME}/taxi/model/${MODEL_NAME}

CURRENT_DATE=`date +%Y%m%d_%H%M%S`
JOB_NAME=train_${MODEL_NAME}_${TIER}_${CURRENT_DATE}

gcloud ai-platform jobs submit training ${JOB_NAME} \
        --stream-logs \
        --job-dir=${MODEL_DIR} \
        --runtime-version=${RUNTIME_VERSION} \
        --region=${REGION} \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH}  \
        --config=../config.yaml \
        -- \
        --train-files=${GCS_TAXI_TRAIN_BIG} \
        --eval-files=${GCS_TAXI_EVAL_BIG} \
	      --train-steps=100000


# Notes:
# use --packages instead of --package-path if gcs location
# add --reuse-job-dir to resume training
