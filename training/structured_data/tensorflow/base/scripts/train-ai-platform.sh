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
echo "Submitting an AI Platform job..."

TF_VERSION=1.13
TIER="BASIC" # BASIC | BASIC_GPU | STANDARD_1 | PREMIUM_1

MODEL_NAME="taxitrips" # change to your model name

PACKAGE_PATH=../trainer # this can be a gcs location to a zipped and uploaded package
TRAIN_FILES=gs://cloud-samples-data/ml-engine/chicago_taxi/training/cloud_taxi_trips_train.csv
EVAL_FILES=gs://cloud-samples-data/ml-engine/chicago_taxi/training/cloud_taxi_trips_eval.csv
MODEL_DIR=gs://${BUCKET_NAME}/taxi/model/${MODEL_NAME}

CURRENT_DATE=`date +%Y%m%d_%H%M%S`
JOB_NAME=train_${MODEL_NAME}_${TIER}_${CURRENT_DATE}

gcloud ai-platform jobs submit training ${JOB_NAME} \
        --job-dir=${MODEL_DIR} \
        --runtime-version=${TF_VERSION} \
        --region=${REGION} \
        --scale-tier=${TIER} \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH}  \
        --config=../config.yaml \
        -- \
        --train-files=${TRAIN_FILES} \
        --eval-files=${EVAL_FILES} \
	    --train-steps=100000


# Notes:
# use --packages instead of --package-path if gcs location
# add --reuse-job-dir to resume training
