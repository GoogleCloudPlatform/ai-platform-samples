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
# This scripts performs local training for a PyTorch model.
echo "Training local ML model"

# IMAGE_REPO_NAME: the image will be stored on Cloud Container Registry
IMAGE_REPO_NAME=pytorch_taxi_container

# IMAGE_TAG: an easily identifiable tag for your docker image
IMAGE_TAG=taxi_pytorch

# IMAGE_URI: the complete URI location for Cloud Container Registry
IMAGE_URI=${IMAGE_REPO_NAME}:${IMAGE_TAG}

# Build the docker image
docker build -f Dockerfile -t ${IMAGE_URI} ./

# These variables are passed to the docker image
# Note: these files have already been copied over when the image was built
TRAIN_FILES=taxi_trips_train.csv
EVAL_FILES=taxi_trips_eval.csv

# Test your docker image locally
echo "Running the Docker Image"
docker run ${IMAGE_URI} \
        --train-files ${TRAIN_FILES} \
        --eval-files ${EVAL_FILES} \
        --num-epochs=1 \
        --batch-size=100 \
        --learning-rate=0.001
