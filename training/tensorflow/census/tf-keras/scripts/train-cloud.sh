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

set -ev

echo "Training cloud ML model"



DATE=$(date '+%Y%m%d_%H%M%S')
MODEL_DIR=/tmp/trained_models/census_$DATE
PACKAGE_PATH=./trainer

# JOB_NAME: the name of your job running on AI Platform.
JOB_NAME=census_$(date +%Y%m%d_%H%M%S)

# JOB_DIR: the output directory
JOB_DIR='gs://$BUCKET_NAME/keras-job-dir' # Change BUCKET_NAME to your bucket's name

# REGION: select a region from https://cloud.google.com/ml-engine/docs/regions
# or use the default '`us-central1`'. The region is where the model will be deployed.
REGION=us-central1

export TRAIN_STEPS=1000
export EVAL_STEPS=100

gcloud ai-platform jobs submit training $JOB_NAME \
  --package-path trainer/ \
  --module-name trainer.task \
  --region $REGION \
  --python-version 3.7 \
  --runtime-version 2.1 \
  --job-dir $JOB_DIR \
  --stream-logs
