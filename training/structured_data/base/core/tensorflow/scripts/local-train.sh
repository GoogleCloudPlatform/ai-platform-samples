#!/bin/bash

echo "Training local ML model"

MODEL_NAME="local_core" # change to your model name

PACKAGE_PATH=trainer
TRAIN_FILES=data/micro_taxi_trips.csv
EVAL_FILES=data/micro_taxi_trips_eval.csv
MODEL_DIR=trained_models/${MODEL_NAME}

gcloud ai-platform local train \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH} \
        -- \
        --train-files=${TRAIN_FILES} \
        --train-size=80000 \
        --num-epochs=10 \
        --batch-size=128 \
        --eval-files=${EVAL_FILES} \
        --learning-rate=0.001 \
        --hidden-units="128,0,0" \
        --layer-sizes-scale-factor=0.5 \
        --num-layers=3 \
        --job-dir=${MODEL_DIR}


ls ${MODEL_DIR}/export/estimate
MODEL_LOCATION=${MODEL_DIR}/export/estimate/$(ls ${MODEL_DIR}/export/estimate | tail -1)
echo ${MODEL_LOCATION}
ls ${MODEL_LOCATION}

gcloud ai-platform local predict --model-dir=${MODEL_LOCATION} --json-instances=data/new-data.json --verbosity debug
