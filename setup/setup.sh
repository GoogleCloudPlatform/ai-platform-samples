#!/usr/bin/env bash
export RUNTIME_VERSION=1.13
export PYTHON_VERSION=3.5
export REGION=us-central1
export PROJECT_ID="your-gcp-project-id"
export BUCKET_NAME="your-gcp-bucket-name"

if [[ ${PROJECT_ID} == "your-gcp-project-id" ]]
then
  echo "Warning: Please set PTOJECT_ID to your gcp Project ID"
fi

if [[ ${BUCKET_NAME} == "your-gcp-bucket-name" ]]
then
  echo "Warning: Please set BUCKET_NAME to an existing GCS bucket"
fi