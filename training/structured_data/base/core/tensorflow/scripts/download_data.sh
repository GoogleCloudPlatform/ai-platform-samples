#!/bin/bash

echo "Download data"

mkdir data && cd data
wget https://storage.cloud.google.com/cloud-samples-data/ml-engine/chicago_taxi/nano_taxi_trips_train.csv
wget https://storage.cloud.google.com/cloud-samples-data/ml-engine/chicago_taxi/nano_taxi_trips_eval.csv
wget https://storage.cloud.google.com/cloud-samples-data/ml-engine/chicago_taxi/new-data.csv
wget https://storage.cloud.google.com/cloud-samples-data/ml-engine/chicago_taxi/new-data.json