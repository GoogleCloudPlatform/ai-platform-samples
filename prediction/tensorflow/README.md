# TensorFlow Estimator - Deploy model

The purpose of this directory is to provide a sample for how you can deploy a
TensorFlow trained model in AI Platform.

*   Run the training example under /training/base/core/tensorflow using the
    `aiplatform-submit-train-job.sh` or `local-train.sh` scripts.
*   Run `aiplatform-deploy-model.sh`


## Scripts:

  [cloud-deploy-model.sh](scripts/cloud-deploy-model.sh)  This script deploys a model in 
  AI platform Prediction. It expects a Saved Model in Google Cloud Storage.

## Versions
Suitable for TensorFlow v1.13.1+
