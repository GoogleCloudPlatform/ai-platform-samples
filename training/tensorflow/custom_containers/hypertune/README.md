
## Introduction

This sample shows how to run hyperparameter tuning jobs on AI Platform with tf estimators inside custom containers [cloudml-hypertune package](https://pypi.org/project/cloudml-hypertune/).

This sample is adapted from [the official samples for tuning ResNet-50 with Cloud TPUs on AI Platform](https://github.com/ultrons/cloudml-samples/tree/master/tpu/hptuning/resnet-hypertune)


## Main Flow
[resnet_main_hypertune.py](resnet/resnet_main_hypertune.py) is executed in the `train_and_eval` mode. Notice that
in this mode the training is executed for set number of steps followed by
evaluation.

## Key Concept(s)
`evaluate` method of the estimator can accept a set of session hooks to  allow
some custom operations/computations during evaluation. In this specific example
the desired task is to communicate the target evaluation metric to the hypertune
service. `HypertuneHook` example provided in this sample accomplishes this task.

Notice also that estimatorSpec for evaluation also specified
`evaluation_metric_ops` to ensure that target tensors to compute the required
metric are present in the evaluation graph with the write tags. 

Tag of the evaluation metric provided the config yaml file the tag in the
evaluation_metric_ops dictionary and the one passed to HypertuneHook constructor
must be consistent.


## Requirements

- Install [Google Cloud Platform SDK](https://cloud.google.com/sdk/).  The SDK includes the commandline tools `gcloud` for submitting training jobs to [AI Platform](https://cloud.google.com/ml-engine/).

- Enable [Cloud Storage](https://cloud.google.com/storage).

## Execution Steps

1. Clone the repository.

    ```
    git clone https://github.com/GoogleCloudPlatform/ai-platform-samples.git
    ```

2. If you do not already have a Cloud Storage bucket, create one to be used for the training job.

    ```
    gsutil mb gs://[YOUR_GCS_BUCKET]
    export GCS_BUCKET="gs://[YOUR_GCS_BUCKET]"
    ```
    This variable is used in the submit_resnet_hypertune.sh script to execute
    the container locally or using ai_platform.

3. Build the custom container using the build.sh script.
    ```
    cd ai-platform-samples/training/tensorflow/custom_containers/hypertune
    bash build.sh
    ```

4. Once the container is built you can test it using submit_resnet_hypertune.sh. 

    ```
    bash  submit_resnet_hypertune.sh --test_local 
    ```

5. Finally, submit the hyperparameter tuning run to ai platform.
   The included script will train ResNet-50 for 1024 steps using a fake dataset.

    ```
    bash submit_resnet_hypertune.sh
    ```
