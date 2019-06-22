# AI Platform Training

## Overview

TensorFlow's Estimator API parses the `TF_CONFIG` environment variable,
if present, and uses the relevant details from `TF_CONFIG` to construct properties
for distributed training, including the cluster spec, task ID, and other
properties.

If your application uses tf.estimator for distributed training, the propagation
of properties to the cluster spec works automatically, as AI Platform sets
`TF_CONFIG` for you.

Similarly, if you run your distributed training application on AI Platform with
a custom container, then AI Platform sets `TF_CONFIG` and populates an environment
variable, `CLUSTER_SPEC`, on each machine.

## Prerequisites

* Follow the instructions in the [setup](../../../../setup) directory in order to setup your environment
* Follow the instructions in the [datasets](../../../../datasets) directory and run [download-taxi.sh](../../../../datasets/download-taxi.sh)
* Create a Python virtual environment and run `pip install -r requirements.txt`
* Run code in `tensorflow/structured/base/trainer/` location using the `config.yaml` in this folder.

## Documentation

Please go to the official AI platform [documentation](https://cloud.google.com/ml-engine/docs/tensorflow/distributed-training-details) for more details.
