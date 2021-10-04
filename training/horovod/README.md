# Run Horovod on AI Platform / Vertex AI

## Overview

This directory provides a sample for how to run Horovod on AI Platform / Vertex AI. In more details, it includes:

* Base container image of AI Platform wrapper for Horovod.
* Example models based on the wrapper.

## Prerequisites

* Setup your project by following the instructions in the [setup](../../setup/) directory.
* [Setup docker with Cloud Container Registry](https://cloud.google.com/container-registry/docs/pushing-and-pulling).
* Change the directory to this sample.

## Examples

### MNIST with Keras

Run the following script to run MNIST training job on AI Platform:

```
MODEL_NAME=mnist GCS_OUTPUT_PATH=<GCS_BUCKET> scripts/train-cloud.sh
```

By default, the script `train-cloud.sh` uses 2 `n1-highmem-96` machines with 8 `nvidia-tesla-v100` GPUs on each machine. Variables `MACHINE_TYPE`, `MACHINE_COUNT`, `GPU_TYPE`, `GPU_COUNT` configure these settings. 

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

## Run Training Jobs on Vertex AI

The examples above run training jobs on AI Platform. To run on Vertex AI, simply use `train-vertex.sh` instead, e.g:

```
MODEL_NAME=mnist GCS_OUTPUT_PATH=<GCS_BUCKET> scripts/train-vertex.sh
```

### Use Reduction Servers

[Reduction Server](https://cloud.google.com/blog/topics/developers-practitioners/optimize-training-performance-reduction-server-vertex-ai) is a feature on Vertex AI to speed up distributed data-parallel training. The `train-vertex.sh` script provides a simple toggle to enable
Reduction Server for Horovod training jobs. To use Reduction Server, set `REDUCER_COUNT` to a positive integer:

```
MODEL_NAME=mnist GCS_OUTPUT_PATH=<GCS_BUCKET> REDUCER_COUNT=6 scripts/train-vertex.sh
```

See the [documentation](https://cloud.google.com/vertex-ai/docs/training/distributed-training#reduce_training_time_with_reduction_server) for details on selecting the number of reducers.

## Bring Your Own Models

Create a folder `<MODEL_NAME>` under the same level as example models (e.g. `mnist` and `maskrcnn`). Create a `Dockerfile` that builds a Docker image based on the `horovod_wrapper` base image. 

The `horovod_wrapper` image depends on the following environment variables:

* `STAGING_DIR`: The directory in the container for staging data from GCS before training. Default is `/input`.
* `OUTPUT_DIR`: The directory in the container from which `horovod_wrapper` will upload to GCS after training. Default is `/output`.
* `STAGE_GCS_PATH`: If set, data will be staged from this path to `STAGING_DIR` before training.
* `GCS_OUTPUT_PATH`: If set, data under `OUTPUT_DIR` will be uploaded to this path after training. 
