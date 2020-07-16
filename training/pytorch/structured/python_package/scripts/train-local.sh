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

# Datasets are set by datasets/download-taxi.sh script
TRAIN_FILES=${GCS_TAXI_TRAIN_SMALL}
EVAL_FILES=${GCS_TAXI_EVAL_SMALL}

python -m trainer.task \
  --train-files ${TRAIN_FILES} \
  --eval-files ${EVAL_FILES} \
  --num-epochs 10 \
  --batch-size 100 \
  --learning-rate 0.001

