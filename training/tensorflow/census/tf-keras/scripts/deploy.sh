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

<<<<<<< HEAD:training/tensorflow/census/tf-keras/scripts/deploy.sh
# This has to be run after train-cloud.sh is successfully executed

REGION="us-central1" # choose a GCP region, e.g. "us-central1". Choose from https://cloud.google.com/ai-platform/training/docs/regions
BUCKET_NAME="" # TODO Change BUCKET_NAME to your bucket name

=======
REGION="us-central1" # choose a GCP region, e.g. "us-central1". Choose from https://cloud.google.com/ai-platform/training/docs/regions
BUCKET_NAME="" # TODO Change BUCKET_NAME to your bucket name

>>>>>>> ebd38b971ba1ac9d0553f99abbe4cb2aac4e0c50:training/tensorflow/census/tf-keras/scripts/cloud-deploy-model.sh
MODEL_NAME="my_first_keras_model" # change to your model name, e.g. "estimator"
MODEL_VERSION="v1" # change to your model version, e.g. "v1"

# Model Binaries corresponds to the tf.estimator.FinalExporter configuration in trainer/experiment.py
MODEL_BINARIES=gs://${BUCKET_NAME}/keras-job-dir/keras_export/
PYTHON_VERSION=3.7
RUNTIME_VERSION=2.1

gsutil ls ${MODEL_BINARIES}

# Delete model version, if previous model version exist.
gcloud ai-platform versions delete ${MODEL_VERSION} --model=${MODEL_NAME}

# Delete model, if previous model exist.
gcloud ai-platform models delete ${MODEL_NAME}

<<<<<<< HEAD:training/tensorflow/census/tf-keras/scripts/deploy.sh
# Deploy model to GCP using regional endpoints.
=======
# Deploy model to GCP
>>>>>>> ebd38b971ba1ac9d0553f99abbe4cb2aac4e0c50:training/tensorflow/census/tf-keras/scripts/cloud-deploy-model.sh
gcloud beta ai-platform models create --region ${REGION} ${MODEL_NAME}

# Deploy model version
gcloud beta ai-platform versions create ${MODEL_VERSION} \
 --model=${MODEL_NAME} \
 --region $REGION \
<<<<<<< HEAD:training/tensorflow/census/tf-keras/scripts/deploy.sh
 --framework TENSORFLOW \
=======
>>>>>>> ebd38b971ba1ac9d0553f99abbe4cb2aac4e0c50:training/tensorflow/census/tf-keras/scripts/cloud-deploy-model.sh
 --origin=${MODEL_BINARIES} \
 --python-version=${PYTHON_VERSION} \
 --runtime-version=${RUNTIME_VERSION} \
 --machine-type "n1-highcpu-2"

# Test predictions
gcloud ai-platform predict \
  --model ${MODEL_NAME} \
  --version ${MODEL_VERSION} \
  --json-instances ../input.json \
  --region=${REGION}