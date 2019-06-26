#!/bin/bash
#
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
#
# This script downloads datasets from GCP to local drive.
set -euxo pipefail

readonly DATA_FOLDER="gs://cloud-samples-data/ml-engine/chicago_taxi"


function err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
  return 1
}


function download_files(){
  local directory=$1
  local size=$2
  echo -e "Downloading $size files in $directory"

  # Check if destination directory exists, otherwise create it.
  if [[ ! -d $directory ]]; then
    mkdir -p $directory
  fi
  cd $directory

  # File paths: gs://cloud-samples-data/ml-engine/chicago_taxi/...
  local gcs_file_path=$DATA_FOLDER/training/$size/taxi_trips.csv
  local gcs_training_path=$DATA_FOLDER/training/$size/taxi_trips_train.csv
  local gcs_eval_path=$DATA_FOLDER/training/$size/taxi_trips_eval.csv
  local gcs_prediction_folder=${DATA_FOLDER}/prediction
  local prediction_file_dict=taxi_trips_prediction_dict.ndjson
  local prediction_file_list=taxi_trips_prediction_list.ndjson

  CWD=`pwd`
  # Copy small and big files from GCS to local directory.
  if [[ $size == 'both' ]]; then
    declare -a arr=("big" "small")
    for element in "${arr[@]}"
    do
      if [[ ! -d $element ]]; then
        mkdir -p $element
      fi
      local gcs_file_path=$DATA_FOLDER/training/$element/taxi_trips.csv
      local gcs_training_path=$DATA_FOLDER/training/$element/taxi_trips_train.csv
      local gcs_eval_path=$DATA_FOLDER/training/$element/taxi_trips_eval.csv
      # Download files from GCS
      gsutil cp $gcs_file_path $element/taxi_trips.csv
      gsutil cp $gcs_training_path $element/taxi_trips_train.csv
      gsutil cp $gcs_eval_path $element/taxi_trips_eval.csv
    done
  else
    if [[ ! -d $size ]]; then
      mkdir -p $size
    fi
    gsutil cp $gcs_file_path $size/taxi_trips.csv
    gsutil cp $gcs_training_path $size/taxi_trips_train.csv
    gsutil cp $gcs_eval_path $size/taxi_trips_eval.csv
  fi

  # Export environmental variables.
  if [[ $size == 'big' || $size == 'both' ]]; then
    # GCS paths
    export GCS_TAXI_BIG=$gcs_file_path
    export GCS_TAXI_TRAIN_BIG=$gcs_file_path
    export GCS_TAXI_EVAL_BIG=$gcs_file_path
    # Local files paths
    export TAXI_TRAIN_BIG=${CWD}/taxi_trips_train.csv
    export TAXI_EVAL_BIG=${CWD}/taxi_trips_eval.csv
  elif [[ $size == 'small' || $size == 'both' ]]; then
    # GCS paths
    export GCS_TAXI_SMALL=$gcs_file_path
    export GCS_TAXI_TRAIN_SMALL=$gcs_file_path
    export GCS_TAXI_EVAL_SMALL=$gcs_file_path
    # Local files paths
    export TAXI_TRAIN_SMALL=${CWD}/taxi_trips_train.csv
    export TAXI_EVAL_SMALL=${CWD}/taxi_trips_eval.csv
  else
    echo -e "Setup your variables manually."
  fi

  # Download prediction files
  echo "Downloading the prediction dataset..."
  if [[ ! -d prediction ]]; then
    mkdir -p prediction
  fi
  # Download files from GCS
  gsutil cp ${gcs_prediction_folder}/$prediction_file_dict ./prediction/$prediction_file_dict
  gsutil cp ${gcs_prediction_folder}/$prediction_file_list ./prediction/$prediction_file_list

  export TAXI_PREDICTION_DICT_NDJSON=${CWD}/prediction/$prediction_file_dict
  export TAXI_PREDICTION_LIST_NDJSON=${CWD}/prediction/$prediction_file_list
  return 0
}


function check_args() {
  # Check number of arguments
  if [[ "$#" -eq "0" ]]; then
    echo "Usage: download-taxi.sh <output-path> [size]" >&2
    echo "    output-path: full path to the output directory." >&2
    echo "    size: either 'small' or 'big'. If omitted, both will be downloaded." >&2
    exit 1
  elif [[ "$#" -eq "1" ]]; then
    # Download both small and big datasets when there is no size provided.
    download_files $1 "both"
  elif [[ "$#" -eq "2" ]]; then
    if [[ "$2" == "big" || "$2" == "small" ]]; then
      download_files $1 $2
    else
      echo "Invalid option size: either 'small' or 'big'"
      exit 1
    fi
  fi
}


main(){
    check_args "$@"
    cd -
}

main "$@"