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
# This script performs local training for a PyTorch model.

echo "Running PyTorch model locally"

# BUCKET_NAME: Change to your bucket name.
BUCKET_NAME=rthallam-demo-project

# JOB_NAME: the name of your job running on AI Platform.
JOB_PREFIX=pytorch_job_bert_classifier
JOB_NAME=${JOB_PREFIX}_$(date +%Y%m%d_%H%M%S)

# JOB_DIR: Where to store prepared package and upload output model.
JOB_DIR=gs://${BUCKET_NAME}/${JOB_PREFIX}/models/${JOB_NAME}

# IMAGE_REPO_NAME: set a local repo name to distinquish our image
IMAGE_REPO_NAME=pytorch_gpu_bert_classifier

# IMAGE_TAG: an easily identifiable tag for your docker image
IMAGE_TAG=imdb_bert_pytorch_gpu

# IMAGE_URI: the complete URI location for the image
IMAGE_URI=${IMAGE_REPO_NAME}:${IMAGE_TAG}

# Build the docker image
docker build -f Dockerfile -t ${IMAGE_URI} ./

# Test your docker image locally
echo "Running the Docker Image"
docker run ${IMAGE_URI} \
    --job-dir ${JOB_DIR} \
    --model-name="finetuned-bert-classifier"

# Verify the model was exported
echo "Verify the model was exported:"
gsutil ls ${JOB_DIR}/