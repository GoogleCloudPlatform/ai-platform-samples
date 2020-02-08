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
set -eo pipefail


download_files() {
    # Download files for testing.
    GCS_FOLDER="gs://cloud-samples-data/ml-engine/chicago_taxi"

    echo -e "Downloading files"
    gsutil cp ${GCS_FOLDER}/training/small/taxi_trips_train.csv data/taxi_trips_train.csv
    gsutil cp ${GCS_FOLDER}/training/small/taxi_trips_eval.csv data/taxi_trips_eval.csv
    gsutil cp ${GCS_FOLDER}/prediction/taxi_trips_prediction_dict.ndjson data/taxi_trips_prediction_dict.ndjson

    # Define ENV for `train-local.sh` script
    export TAXI_TRAIN_SMALL=data/taxi_trips_train.csv
    export TAXI_EVAL_SMALL=data/taxi_trips_eval.csv
    export TAXI_PREDICTION_DICT_NDJSON=data/taxi_trips_prediction_dict.ndjson
}


run_tests() {
    # Run base tests.
    echo -e "Running code tests in $(pwd)."
    download_files
    # Run local training and local prediction
    source scripts/train-local.sh
}


main(){
    cd "${KOKORO_ARTIFACTS_DIR}"/github/ai-platform-samples/"${CAIP_TEST_DIR}"
    run_tests
    echo -e "Test was successful"
}

main
