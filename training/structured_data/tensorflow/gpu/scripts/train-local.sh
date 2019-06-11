#!/bin/bash

echo "Training local ML model"

MODEL_NAME="local_gpu" # Change to your model name

PACKAGE_PATH=trainer
# Run ./download-taxi.sh under datasets folder or set the value directly.
TRAIN_FILES=${LOCAL_TAXI_TRAINING}
EVAL_FILES=${LOCAL_TAXI_EVALUATION}
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
