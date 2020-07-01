# PyTorch - Python Package Training

## Overview
The purpose of this directory is to provide a sample for how you can package a
PyTorch training model to submit it to AI Platform using pre-built PyTorch
containers. This sample makes it easier to organize your code, and to adapt it
to your dataset. In more details, the sample covers the following functionality:

* Metadata to define your dataset, along with the problem type (Classification).
* Standard implementation of input, parsing, and serving functions.
* Automatic feature columns creation based on the metadata (and normalization
  stats).
* Train, evaluate, and export the model.
* Parameterization of the experiment.

Although this sample provides a standard implementation of this functionality,
you can customize these parts with your own implementation.

## Prerequisites
* Setup your project by following the instructions in the
  [setup](../../../../../setup/) directory.
* [OPTIONAL] Download the datasets using
  [download-taxi.sh](../../../../datasets/download-taxi.sh) located in the
  [datasets](../../../../datasets) folder. The sample script only requires the
  `GCS_TAXI_TRAIN_BIG` AND `GCS_TAXI_EVAL_BIG` environment variables to be set.
* Change directories to this sample.

## Sample Structure

* `trainer` directory: all Python modules to train the model.
* `scripts` directory: command-line script to train the model on AI Platform.

### Trainer Modules
| File Name | Purpose |
| :-------- | :------ |
| [metadata.py](trainer/metadata.py) | Defines: 1) task type, 2) input data
header, 3) numeric and categorical feature names, and 4) target feature name
(and labels, for a classification task) |
| [inputs.py](trainer/inputs.py) | Includes: 1) data input functions to read
data from csv files, 2) parsing functions to convert csv to tensors, 3) function
to implement your custom features processing and creation functionality, and 4)
prediction functions (for serving the model) that accepts CSV, JSON, and
tf.example instances. |
| [model.py](trainer/model.py) | Includes: 1) function to create
DNNLinearCombinedRegressor, and 2) DNNLinearCombinedClassifier. |
| [experiment.py](trainer/experiment.py) | Runs the model training and
evaluation experiment, and exports the final model. |
| [task.py](trainer/task.py) | Includes: 1) Initialise and parse task arguments
(hyper parameters), and 2) Entry point to the trainer. |

### Scripts

* [train-cloud.sh](scripts/train-cloud.sh) This script submits a training job to
  AI Platform.

## How to run
Once the prerequisites are satisfied, update the `BUCKET_NAME` environment
variable in `scripts/train-cloud.sh`. You may then run the following script to
submit an AI Platform Training job:
```
source ./scripts/train-cloud.sh
```

### Versions
This script uses the pre-built PyTorch container for PyTorch 1.4.
* `gcr.io/cloud-ml-public/training/pytorch-cpu.1-4`

