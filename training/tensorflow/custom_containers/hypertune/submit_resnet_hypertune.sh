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
# Run AI Platform training remotely.

export PROJECT_ID=$(gcloud config list project --format "value(core.project)")
export IMAGE_REPO_NAME=estimator-hypertune
export IMAGE_TAG=latest
export IMAGE_URI=gcr.io/$PROJECT_ID/$IMAGE_REPO_NAME:$IMAGE_TAG

#GCS_BUCKET is expected as en environment variable.
#GCS_BUCKET=gs://tpu-exp-02272020
BUCKET=$GCS_BUCKET

now=$(date +"%Y%m%d_%H%M%S")

JOB_NAME="resnet_hypertune_$now"

REGION=us-central1
DATA_DIR=gs://cloud-tpu-test-datasets/fake_imagenet
OUTPUT_PATH=$BUCKET"/"$JOB_NAME

if [ "$1" = "--test_local" ]; then
  docker run "$IMAGE_URI" \
    --data_dir=$DATA_DIR \
    --model_dir="$OUTPUT_PATH" \
    --resnet_depth=50 \
    --train_steps=1024
else
  gcloud ai-platform jobs submit training "$JOB_NAME" \
    --scale-tier CUSTOM \
    --master-machine-type n1-highmem-8 \
    --master-accelerator count=1,type=nvidia-tesla-v100 \
    --region "$REGION" \
    --master-image-uri "$IMAGE_URI" \
    --config config_resnet_hypertune.yaml \
    -- \
    --data_dir="$DATA_DIR" \
    --model_dir="$OUTPUT_PATH" \
    --resnet_depth=50 \
    --train_steps=1024
fi
