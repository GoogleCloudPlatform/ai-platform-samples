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
echo "Downloading data"

export DATA_FOLDER="https://storage.cloud.google.com/cloud-samples-data/ml-engine/"

mkdir data && cd data

wget "${DATA_FOLDER}"/chicago_taxi/nano_taxi_trips_train.csv
wget "${DATA_FOLDER}"/chicago_taxi/nano_taxi_trips_eval.csv
wget "${DATA_FOLDER}"/chicago_taxi/new-data.csv
wget "${DATA_FOLDER}"/chicago_taxi/new-data.json