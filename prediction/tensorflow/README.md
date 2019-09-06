# TensorFlow Estimator - Deploy model

The purpose of this directory is to provide a sample for how you can deploy a
TensorFlow trained model in AI Platform with GPU.

*   Run the training example under `/training/tensorflow/structured/base/scripts` using the
    `train-cloud.sh` or `train-local.sh` scripts.
*   Run either:
    - `cloud-deploy-model.sh`
    - `cloud-deploy-model-gpu.sh`

## GPU support

Now if you want to deploy a new model and use GPUs, now is as simple as 
define the machine type and select which accelerator you want to use for
your new model. 

Upgrade to the latest version of Google Cloud SDK

```
gcloud components update
```

Define the machine-type which will be handling these requests. In this case we enabled a `n1-standard-4` which is a Standard machine type with 4 vCPUs and 15 GB of memory. The full list is available [here](https://cloud.google.com/compute/docs/machine-types). 

After you update to new gcloud SDK version you will see the `--accelerator` option available. 
The type of the accelerator can only be one of the following: 

```
nvidia-tesla-k80
nvidia-tesla-p100
nvidia-tesla-p4
nvidia-tesla-t4 
nvidia-tesla-v100
tpu-v2 (Not covered in this document)
```

Create a new model deployment with GPU:

```
gcloud alpha ai-platform versions create gpu_v1 \
 --model=model_inference \
 --runtime-version=1.14 \
 --python-version=3.5 \
 --framework=tensorflow \
 --machine-type="n1-standard-4" \
 --accelerator=count=4,type=nvidia-tesla-t4 \
 --origin=gs://google_cloud_bucket/model/
```

**Note:** This feature is in Alpha. If you want to get access contact: <cloudml-feedback@google.com>

## Scripts

  [cloud-deploy-model.sh](structured/scripts/cloud-deploy-model.sh)  This script deploys a model in 
  AI platform Prediction. It expects a Saved Model in Google Cloud Storage.
  
  [cloud-deploy-model-gpu.sh](structured/scripts/cloud-deploy-model-gpu.sh) This script deploys a model in 
  AI platform Prediction using GPU. It expects a Saved Model in Google Cloud Storage.

## Versions
Suitable for TensorFlow v1.13.1+

## Feedback

We’re happy to hear from you if we need to enable additional Compute Engine machine types. If you desire a machine type not available here, please contact <cloudml-feedback@google.com>
