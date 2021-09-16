#!/bin/bash
# Copyright 2021 Google LLC
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

set -e

# This scripts performs cloud training for a Horovod model.
echo "Training Vertex AI model"

# MODEL_NAME: the name of model directory. The directory should contain 
# the Dockerfile.
MODEL_NAME=${MODEL_NAME:-mnist}

# MACHINE_TYPE: type of machines for training
MACHINE_TYPE=${MACHINE_TYPE:-n1-highmem-96}

# MACHINE_COUNT: number of workers (master included)
MACHINE_COUNT=${MACHINE_COUNT:-2}

# REDUCER_COUNT: number of reducers
REDUCER_COUNT=${REDUCER_COUNT:-0}

# GPU_TYPE: type of GPU
GPU_TYPE=${GPU_TYPE:-NVIDIA_TESLA_T4}

# GPU_COUNT: number of GPUs per machine
GPU_COUNT=${GPU_COUNT:-4}

# IMAGE_REPO_NAME: the image will be stored on Cloud Container Registry
IMAGE_REPO_NAME=horovod_${MODEL_NAME}

PROJECT_ID=${PROJECT_ID:-$(gcloud config list project --format "value(core.project)")}

# IMAGE_URI: the complete URI location for Cloud Container Registry
IMAGE_URI=gcr.io/${PROJECT_ID}/${IMAGE_REPO_NAME}

# JOB_NAME: the name of your job running on AI Platform.
JOB_NAME=${MODEL_NAME}_$(date +%Y%m%d_%H%M%S)

# REGION: select a region from https://cloud.google.com/ml-engine/docs/regions
# or use the default '`us-central1`'. The region is where the model will be deployed.
REGION=us-central1

echo "Building Horovod container image"

# Build the wrapper docker image
docker build -f base/Dockerfile -t horovod-wrapper base/

# Build the docker image
docker build -f ${MODEL_NAME}/Dockerfile \
    --build-arg GCS_OUTPUT_PATH=${GCS_OUTPUT_PATH} \
    --build-arg STAGE_GCS_PATH=${STAGE_GCS_PATH} \
    -t ${IMAGE_URI} ./

# Deploy the docker image to Cloud Container Registry
docker push ${IMAGE_URI}

# Submit your training job
echo "Submitting the training job"

if [ "${MACHINE_COUNT}" -gt "1" ]; then
    WORKER_CONFIG="--worker-pool-spec=machine-type=${MACHINE_TYPE},replica-count=$((MACHINE_COUNT - 1)),container-image-uri=${IMAGE_URI},accelerator-type=${GPU_TYPE},accelerator-count=${GPU_COUNT}"
else
    WORKER_CONFIG=""
fi

if [ "${REDUCER_COUNT}" -gt "0" ] && [ "${MACHINE_COUNT}" -gt "1" ]; then
    REDUCER_CONFIG="--worker-pool-spec=machine-type=n1-highcpu-16,replica-count=${REDUCER_COUNT},container-image-uri=us-docker.pkg.dev/vertex-ai-restricted/training/reductionserver:latest"
else
    REDUCER_CONFIG=""
fi

gcloud beta ai custom-jobs create \
    --display-name ${JOB_NAME} \
    --region ${REGION} \
    --worker-pool-spec=machine-type=${MACHINE_TYPE},replica-count=1,container-image-uri=${IMAGE_URI},accelerator-type=${GPU_TYPE},accelerator-count=${GPU_COUNT} \
    ${WORKER_CONFIG} \
    ${REDUCER_CONFIG}


# Verify the model was exported
echo "Verify the model was exported:"
gsutil ls ${GCS_OUTPUT_PATH}
