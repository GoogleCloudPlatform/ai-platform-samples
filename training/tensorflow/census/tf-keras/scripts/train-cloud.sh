#!/bin/bash
# Copyright 2020 Google LLC
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
# This scripts performs cloud training for a TensorFlow model.

set -v

echo "Training Cloud ML model"

DATE=$(date '+%Y%m%d_%H%M%S')

# JOB_NAME: the name of your job running on AI Platform.
JOB_NAME=census_$(date +%Y%m%d_%H%M%S)

# JOB_DIR: the output directory
JOB_DIR=gs://${BUCKET_NAME}/keras-job-dir # TODO Change BUCKET_NAME to your bucket name

# REGION: select a region from https://cloud.google.com/ai-platform/training/docs/regions
# or use the default '`us-central1`'. The region is where the model will be deployed.
REGION=us-central1
PYTHON_VERSION=3.7
RUNTIME_VERSION=2.1
TRAIN_STEPS=1000
EVAL_STEPS=100

CONFIG_FILE=hptuning_config.yaml # Add --config ${CONFIG_FILE} for Hyperparameter tuning


gcloud ai-platform jobs submit training "${JOB_NAME}" \
  --package-path trainer/ \
  --module-name trainer.task \
  --region ${REGION} \
  --python-version $PYTHON_VERSION \
  --runtime-version $RUNTIME_VERSION \
  --job-dir "${JOB_DIR}" \
  --stream-logs -- \
  --train-steps=${TRAIN_STEPS} \
  --eval-steps=${EVAL_STEPS} \
