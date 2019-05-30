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

export DATA_FOLDER="gs://cloud-samples-data/ml-engine"

mkdir -p $1 && cd $1

ROOT="$(printf "%s\n" "$(pwd)")"

if [[ $2 == 'big' ]]; then
  echo "Downloading the big dataset..."
  gsutil cp ${DATA_FOLDER}/chicago_taxi/big_taxi_trips_train.csv big_taxi_trips_train.csv
  gsutil cp ${DATA_FOLDER}/chicago_taxi/big_taxi_trips_eval.csv big_taxi_trips_eval.csv

  export BIG_TAXI_TRAINING=${ROOT}/big_taxi_trips_train.csv
  export BIG_TAXI_EVALUATION=${ROOT}/big_taxi_trips_eval.csv
elif [[ $2 == 'small' ]]; then
  echo "Downloading the small dataset..."
  gsutil cp ${DATA_FOLDER}/chicago_taxi/small_taxi_trips_train.csv small_taxi_trips_train.csv
  gsutil cp ${DATA_FOLDER}/chicago_taxi/small_taxi_trips_eval.csv small_taxi_trips_eval.csv

  export SMALL_TAXI_TRAINING=${ROOT}/small_taxi_trips_train.csv
  export SMALL_TAXI_EVALUATION=${ROOT}/small_taxi_trips_eval.csv
else
  echo "Downloading the big dataset..."
  gsutil cp ${DATA_FOLDER}/chicago_taxi/big_taxi_trips_train.csv big_taxi_trips_train.csv
  gsutil cp ${DATA_FOLDER}/chicago_taxi/big_taxi_trips_eval.csv big_taxi_trips_eval.csv

  export BIG_TAXI_TRAINING=${ROOT}/big_taxi_trips_train.csv
  export BIG_TAXI_EVALUATION=${ROOT}/big_taxi_trips_eval.csv

  echo "Downloading the small dataset..."
  gsutil cp ${DATA_FOLDER}/chicago_taxi/small_taxi_trips_train.csv small_taxi_trips_train.csv
  gsutil cp ${DATA_FOLDER}/chicago_taxi/small_taxi_trips_eval.csv small_taxi_trips_eval.csv

  export SMALL_TAXI_TRAINING=${ROOT}/small_taxi_trips_train.csv
  export SMALL_TAXI_EVALUATION=${ROOT}/small_taxi_trips_eval.csv
fi

echo "Downloading the prediction dataset..."
gsutil cp ${DATA_FOLDER}/chicago_taxi/taxi_trips_prediction.json taxi_trips_prediction.json
gsutil cp ${DATA_FOLDER}/chicago_taxi/taxi_trips_prediction.csv taxi_trips_prediction.csv

export TAXI_PREDICTION_JSON=${ROOT}/taxi_trips_prediction.json
export TAXI_PREDICTION_CSV=${ROOT}/taxi_trips_prediction.csv

cd -


