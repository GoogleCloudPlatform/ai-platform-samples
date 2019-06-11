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

if [[ -z "$1" ]]; then
  echo "Usage: download-taxi.sh <output-path> [size]"
  echo "    output-path: full path to the output directory"
  echo "    size: either 'small' or 'big'. If omitted, both will be downloaded"
  exit 1
fi

export DATA_FOLDER="gs://cloud-samples-data/ml-engine/chicago_taxi"
export TRAIN_FOLDER=${DATA_FOLDER}/training
export PREDICTION_FOLDER=${DATA_FOLDER}/prediction

export GCS_TAXI_BIG=${TRAIN_FOLDER}/big/taxi_trips.csv
export GCS_TAXI_TRAIN_BIG=${TRAIN_FOLDER}/big/taxi_trips_train.csv
export GCS_TAXI_EVAL_BIG=${TRAIN_FOLDER}/big/taxi_trips_train.csv

export GCS_TAXI_SMALL=${TRAIN_FOLDER}/small/taxi_trips.csv
export GCS_TAXI_TRAIN_SMALL=${TRAIN_FOLDER}/small/taxi_trips_train.csv
export GCS_TAXI_EVAL_SMALL=${TRAIN_FOLDER}/small/taxi_trips_train.csv


mkdir -p $1 && cd $1

ROOT="$(printf "%s\n" "$(pwd)")"

if [[ $2 == 'big' ]]; then
  echo "Downloading the big dataset..."
  mkdir big
  gsutil cp ${GCS_TAXI_TRAIN_BIG} big/taxi_trips_train.csv
  gsutil cp ${GCS_TAXI_EVAL_BIG} bigtaxi_trips_eval.csv

  export TAXI_TRAIN_BIG=${ROOT}/taxi_trips_train.csv
  export TAXI_EVAL_BIG=${ROOT}/taxi_trips_eval.csv
elif [[ $2 == 'small' ]]; then
  echo "Downloading the small dataset..."
  mkdir small
  gsutil cp ${GCS_TAXI_TRAIN_SMALL} small/taxi_trips_train.csv
  gsutil cp ${GCS_TAXI_EVAL_SMALL} small/taxi_trips_eval.csv

  export TAXI_TRAIN_SMALL=${ROOT}/small/taxi_trips_train.csv
  export TAXI_EVAL_SMALL=${ROOT}/small/taxi_trips_eval.csv
else
  echo "Downloading the big dataset..."
  mkdir big
  gsutil cp ${GCS_TAXI_TRAIN_BIG} big/taxi_trips_train.csv
  gsutil cp ${GCS_TAX_EVAL_BIG} bigtaxi_trips_eval.csv

  export TAXI_TRAIN_BIG=${ROOT}/taxi_trips_train.csv
  export TAXI_EVAL_BIG=${ROOT}/taxi_trips_eval.csv

  echo "Downloading the small dataset..."
  mkdir small
  gsutil cp ${GCS_TAXI_TRAIN_SMALL} small/taxi_trips_train.csv
  gsutil cp ${GCS_TAXI_EVAL_SMALL} small/taxi_trips_eval.csv

  export TAXI_TRAIN_SMALL=${ROOT}/small/taxi_trips_train.csv
  export TAXI_EVAL_SMALL=${ROOT}/small/taxi_trips_eval.csv
fi

echo "Downloading the prediction dataset..."
mkdir prediction
gsutil cp ${PREDICTION_FOLDER}/taxi_trips_prediction.json ./prediction/taxi_trips_prediction.json
gsutil cp ${PREDICTION_FOLDER}/taxi_trips_prediction_list.txt ./prediction/taxi_trips_prediction_list.txt

export TAXI_PREDICTION_JSON=${ROOT}/prediction/taxi_trips_prediction.json
export TAXI_PREDICTION_LIST=${ROOT}/prediction/taxi_trips_prediction_list.txt

cd -


