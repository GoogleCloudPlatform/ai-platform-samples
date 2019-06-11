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

export DATA_FOLDER="gs://cloud-samples-data/ml-engine/chicago_taxi/training"

mkdir -p $1 && cd $1

CWD="$(printf "%s\n" "$(pwd)")"

if [[ $2 == 'cloud' ]]; then
  echo "Downloading the Cloud dataset..."
  gsutil cp ${DATA_FOLDER}/cloud_taxi_trips_train.csv cloud_taxi_trips_train.csv
  gsutil cp ${DATA_FOLDER}/cloud_taxi_trips_eval.csv cloud_taxi_trips_eval.csv

  export CLOUD_TAXI_TRAINING=${CWD}/cloud_taxi_trips_train.csv
  export CLOUD_TAXI_EVALUATION=${CWD}/cloud_taxi_trips_eval.csv

elif [[ $2 == 'local' ]]; then
  echo "Downloading the Local dataset..."
  gsutil cp ${DATA_FOLDER}/local_taxi_trips_train.csv local_taxi_trips_train.csv
  gsutil cp ${DATA_FOLDER}/local_taxi_trips_eval.csv local_taxi_trips_eval.csv

  export LOCAL_TAXI_TRAINING=${CWD}/local_taxi_trips_train.csv
  export LOCAL_TAXI_EVALUATION=${CWD}/local_taxi_trips_eval.csv

else
  echo "Downloading the Cloud dataset..."
  gsutil cp ${DATA_FOLDER}/cloud_taxi_trips_train.csv cloud_taxi_trips_train.csv
  gsutil cp ${DATA_FOLDER}/cloud_taxi_trips_eval.csv cloud_taxi_trips_eval.csv

  export CLOUD_TAXI_TRAINING=${CWD}/cloud_taxi_trips_train.csv
  export CLOUD_TAXI_EVALUATION=${CWD}/cloud_taxi_trips_eval.csv

  echo "Downloading the Local dataset..."
  gsutil cp ${DATA_FOLDER}/local_taxi_trips_train.csv local_taxi_trips_train.csv
  gsutil cp ${DATA_FOLDER}/local_taxi_trips_eval.csv local_taxi_trips_eval.csv

  export LOCAL_TAXI_TRAINING=${CWD}/local_taxi_trips_train.csv
  export LOCAL_TAXI_EVALUATION=${CWD}/local_taxi_trips_eval.csv
fi

echo "Downloading the prediction dataset..."
gsutil cp ${DATA_FOLDER}/taxi_trips_prediction.json taxi_trips_prediction.json
gsutil cp ${DATA_FOLDER}/taxi_trips_prediction.csv taxi_trips_prediction_list.txt

export TAXI_PREDICTION_JSON=${CWD}/taxi_trips_prediction.json
export TAXI_PREDICTION_CSV=${CWD}/taxi_trips_prediction_list.txt

cd -


