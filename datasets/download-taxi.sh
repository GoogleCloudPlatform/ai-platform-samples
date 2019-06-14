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

set -v -e

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
export GCS_TAXI_EVAL_BIG=${TRAIN_FOLDER}/big/taxi_trips_eval.csv

export GCS_TAXI_SMALL=${TRAIN_FOLDER}/small/taxi_trips.csv
export GCS_TAXI_TRAIN_SMALL=${TRAIN_FOLDER}/small/taxi_trips_train.csv
export GCS_TAXI_EVAL_SMALL=${TRAIN_FOLDER}/small/taxi_trips_eval.csv

if [[ ! -d $1 ]]; then
  mkdir -p $1
fi
cd $1


CWD="$(printf "%s\n" "$(pwd)")"

if [[ $2 == 'big' ]]; then
  echo "Downloading the big dataset..."
  if [[ ! -d big ]]; then
    mkdir -p big
  fi
  gsutil cp ${GCS_TAXI_TRAIN_BIG} big/taxi_trips_train.csv
  gsutil cp ${GCS_TAXI_EVAL_BIG} bigtaxi_trips_eval.csv

  export TAXI_TRAIN_BIG=${CWD}/taxi_trips_train.csv
  export TAXI_EVAL_BIG=${CWD}/taxi_trips_eval.csv
elif [[ $2 == 'small' ]]; then
  echo "Downloading the small dataset..."
  if [[ ! -d small ]]; then
    mkdir -p small
  fi
  gsutil cp ${GCS_TAXI_TRAIN_SMALL} small/taxi_trips_train.csv
  gsutil cp ${GCS_TAXI_EVAL_SMALL} small/taxi_trips_eval.csv

  export TAXI_TRAIN_SMALL=${CWD}/small/taxi_trips_train.csv
  export TAXI_EVAL_SMALL=${CWD}/small/taxi_trips_eval.csv
else
  echo "Downloading the big and the small datasets..."
  if [[ ! -d big ]]; then
    mkdir -p big
  fi
  gsutil cp ${GCS_TAXI_TRAIN_BIG} big/taxi_trips_train.csv
  gsutil cp ${GCS_TAXI_EVAL_BIG} big/taxi_trips_eval.csv

  export TAXI_TRAIN_BIG=${CWD}/taxi_trips_train.csv
  export TAXI_EVAL_BIG=${CWD}/taxi_trips_eval.csv

  if [[ ! -d small ]]; then
    mkdir -p small
  fi
  gsutil cp ${GCS_TAXI_TRAIN_SMALL} small/taxi_trips_train.csv
  gsutil cp ${GCS_TAXI_EVAL_SMALL} small/taxi_trips_eval.csv

  export TAXI_TRAIN_SMALL=${CWD}/small/taxi_trips_train.csv
  export TAXI_EVAL_SMALL=${CWD}/small/taxi_trips_eval.csv
fi

echo "Downloading the prediction dataset..."
if [[ ! -d prediction ]]; then
  mkdir -p prediction
fi
gsutil cp ${PREDICTION_FOLDER}/taxi_trips_prediction_dict.ndjson ./prediction/taxi_trips_prediction_dict.ndjson
gsutil cp ${PREDICTION_FOLDER}/taxi_trips_prediction_list.ndjson ./prediction/taxi_trips_prediction_list.ndjson

export TAXI_PREDICTION_DICT_NDJSON=${CWD}/prediction/taxi_trips_prediction_dict.ndjson
export TAXI_PREDICTION_LIST_NDJSON=${CWD}/prediction/taxi_trips_prediction_list.ndjson

cd -
