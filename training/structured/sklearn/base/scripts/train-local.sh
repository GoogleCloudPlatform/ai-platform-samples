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
echo "Training local ML model"

MODEL_NAME="sklearn-taxi" # Change to your model name, e.g. "estimator"

PACKAGE_PATH=../trainer
MODEL_DIR=../trained_models/${MODEL_NAME}

gcloud ai-platform local train \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH} \
        -- \
        --job-dir=${MODEL_DIR} \
        --input=${SMALL_TAXI_TRAINING} \
        --n-estimators=20 \
        --max-depth=3


ls ${MODEL_DIR}
MODEL_LOCATION=${MODEL_DIR}/model
echo ${MODEL_LOCATION}
ls ${MODEL_LOCATION}

gcloud ai-platform local predict --model-dir=${MODEL_LOCATION} --json-instances=$TAXI_PREDICTION_CSV --verbosity debug
