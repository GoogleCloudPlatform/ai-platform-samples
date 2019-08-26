#!/bin/bash
# Copyright 2019 Google LLC. All Rights Reserved.
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
# This scripts performs local training for a TensorFlow model.
set -ev
echo "Training local ML model"

MODEL_NAME="tensorflow_taxi" # Change to your model name, e.g. "estimator"

PACKAGE_PATH=./trainer
MODEL_DIR=/tmp/trained_models/${MODEL_NAME}
# Run ./download-taxi.sh under datasets folder or set the value directly.

gcloud ai-platform local train \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH} \
        -- \
        --train-files=${TAXI_TRAIN_SMALL} \
        --train-size=80000 \
        --num-epochs=10 \
        --batch-size=128 \
        --eval-files=${TAXI_EVAL_SMALL} \
        --learning-rate=0.001 \
        --hidden-units="128,0,0" \
        --layer-sizes-scale-factor=0.5 \
        --num-layers=3 \
        --job-dir=${MODEL_DIR}


ls ${MODEL_DIR}/export/estimate
MODEL_LOCATION=${MODEL_DIR}/export/estimate/$(ls ${MODEL_DIR}/export/estimate | tail -1)
echo ${MODEL_LOCATION}
ls ${MODEL_LOCATION}

# Open issue: https://stackoverflow.com/questions/48824381/gcloud-ml-engine-local-predict-runtimeerror-bad-magic-number-in-pyc-file
# Verify local prediction
# gcloud ai-platform local predict --model-dir=${MODEL_LOCATION} --json-instances=${TAXI_PREDICTION_DICT_NDJSON} --verbosity debug

