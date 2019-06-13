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

#!/bin/bash

echo "Training local ML model"

MODEL_NAME="sklearn-taxi"

PACKAGE_PATH=./trainer
MODEL_DIR=./trained/${MODEL_NAME}

gcloud ai-platform local train \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH} \
        --job-dir=${MODEL_DIR} \
        -- \
        --log-level DEBUG \
        --input=${TAXI_TRAIN_SMALL} \
        --n-estimators=20 \
        --max-depth=3

# Notes:
# TAXI_TRAIN_SMALL is set by datasets/downlaod-taxi.sh script
