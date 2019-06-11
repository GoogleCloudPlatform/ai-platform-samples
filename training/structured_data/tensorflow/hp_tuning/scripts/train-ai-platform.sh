#!/bin/bash

echo "Submitting an AI Platform job..."

TF_VERSION=1.13
REGION="choose-gcp-region" # choose a gcp region from https://cloud.google.com/ml-engine/docs/tensorflow/regions
TIER="BASIC" # BASIC | BASIC_GPU | STANDARD_1 | PREMIUM_1
BUCKET="you-bucket-name" # change to your bucket name

MODEL_NAME="your_model_name" # change to your model name

PACKAGE_PATH=trainer # this can be a gcs location to a zipped and uploaded package
TRAIN_FILES=gs://cloud-samples-data/ml-engine/chicago_taxi/training/cloud_taxi_trips_train.csv
EVAL_FILES=gs://cloud-samples-data/ml-engine/chicago_taxi/training/cloud_taxi_trips_eval.csv
MODEL_DIR=gs://${BUCKET}/path/to/models/${MODEL_NAME}

CURRENT_DATE=`date +%Y%m%d_%H%M%S`
JOB_NAME=train_${MODEL_NAME}_${TIER}_${CURRENT_DATE}

gcloud ai-platform jobs submit training ${JOB_NAME} \
        --job-dir=${MODEL_DIR} \
        --runtime-version=TF_VERSION \
        --region=${REGION} \
        --scale-tier=${TIER} \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH}  \
        --config=hpt_config.yaml \
        -- \
        --train-files=${TRAIN_FILES} \
        --eval-files=${EVAL_FILES} \
	    --train-steps=800000


# Notes:
# use --packages instead of --package-path if gcs location
# add --reuse-job-dir to resume training
