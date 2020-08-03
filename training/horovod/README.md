# Run Horovod on AI Platform

## Overview

This directory provides a sample for how to run Horovod on AI Platform. In more details, it includes:

* Base container image of AI Platform wrapper for Horovod.
* Example models based on the wrapper.

## Prerequisites

* Setup your project by following the instructions in the [setup](../../setup/) directory.
* [Setup docker with Cloud Container Registry](https://cloud.google.com/container-registry/docs/pushing-and-pulling).
* Change the directory to this sample.

## Examples

### MNIST with Keras

Run the following script

```
MODEL_NAME=mnist GCS_OUTPUT_PATH=<GCS_BUCKET> scripts/train-cloud.sh
```

By default, the script `train-cloud.sh` uses 2 `n1-highmem-96` machines with 4 `nvidia-tesla-t4` GPUs on each machine. Variables `MACHINE_TYPE`, `MACHINE_COUNT`, `GPU_TYPE`, `GPU_COUNT` configure these settings. 

### MaskRCNN with Tensorpack

Prepare the dataset on a GCS bucket so that there are the following directories in `<COCO_DATASET>`:

```
  ImageNet-R50-AlignPadding.npz  annotations/  train2017/  val2017/
```

Run the following script

```
MODEL_NAME=maskrcnn STAGE_GCS_PATH=<COCO_DATASET> GCS_OUTPUT_PATH=<GCS_BUCKET> scripts/train-cloud.sh
```

### BERT

Configure the hyperparameters (e.g. `num_train_epochs`, `learning_rate`, `train_batch_size`, `max_seq_length`, `doc_stride`, etc.) in `bert/Dockerfile`. Run the following script

```
MODEL_NAME=bert GCS_OUTPUT_PATH=<GCS_BUCKET> scripts/train-cloud.sh
```

## Bring Your Own Models

Create a folder `<MODEL_NAME>` under the same level as example models (e.g. `mnist` and `maskrcnn`). Create a `Dockerfile` that builds a Docker image based on the `horovod_wrapper` base image. 

The `horovod_wrapper` image depends on the following environment variables:

* `STAGING_DIR`: The directory in the container for staging data from GCS before training. Default is `/input`.
* `OUTPUT_DIR`: The directory in the container from which `horovod_wrapper` will upload to GCS after training. Default is `/output`.
* `STAGE_GCS_PATH`: If set, data will be staged from this path to `STAGING_DIR` before training.
* `GCS_OUTPUT_PATH`: If set, data under `OUTPUT_DIR` will be uploaded to this path after training. 
