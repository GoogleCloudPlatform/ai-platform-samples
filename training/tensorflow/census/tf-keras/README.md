# Getting started: Training and prediction with Keras in AI Platform

This code uses [`tf.keras`](https://www.tensorflow.org/guide/keras) to
train a classifier on the [Census Income Data
Set](https://archive.ics.uci.edu/ml/datasets/Census+Income). It's
designed so you can run the training on
[Cloud AI Platform](https://cloud.google.com/ml-engine).


## Overview

The purpose of this directory is to provide a sample for how you can package a
TensorFlow training model to submit it to AI Platform. The sample makes it
easier to organise your code, and to adapt it to your dataset. In more details,
the template covers the following functionality:

*   Metadata to define your dataset, along with the problem type (Classification).
*   Standard implementation of input, parsing, and serving functions.
*   Automatic feature columns creation based on the metadata (and normalization stats).
*   Binary classification model construction using tf.keras.
*   Train, evaluate, and export the model.
*   Parameterization of the experiment.

Although this sample provides standard implementation to different
functionality, you can customise these parts with your own implementation.

## Prerequisites

* Create a Python 3 virtual environment and activate it.
* Change the directory to this sample and run: 

  ```
  python setup.py install
  ```
  
  Optional: You can also run:
  ```
  pip install -r requirements.txt
  ```

**Note:** These instructions are used for local testing. When you submit a training job, no code will be executed on 
your local machine.
  

## Sample Structure

* `trainer` directory: with all the python modules to adapt to your data
* `scripts` directory: command-line scripts to train the model locally or on AI Platform
* `requirements.txt`: containing all the required python packages for this sample 
* `hptuning_config.yaml`: for hyper-parameter tuning and specifying the
  AI Platform scale-tier

### Trainer Template Modules

File Name                                         | Purpose  | Do You Need to Change?
:------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------
[model.py](trainer/model.py)                      | Includes: 1) A function to create a Binary Classification model. | **No, unless** you want to change something in the estimator, e.g., activation functions, optimizers, etc..
[predictor.py](trainer/predictor.py)              | Includes: 1) A function to implement your custom pre-processing during prediction time, and 2) prediction functions (for serving the model) |  **Maybe**, if you want to implement any custom pre-processing during prediction time.
[preprocess.py](trainer/preprocess.py)            | Creates: 1) A Pickle preprocessor to calculate z-scores and preprocess predictions | **Maybe**, if you want to implement any custom pre-processing during prediction time.
[task.py](trainer/task.py)                        | Includes: 1) Initialise and parse task arguments (hyper parameters), and 2) Entry point to the trainer. | **No, unless** you want to add/remove parameters, or change parameter default values.
[util.py](trainer/util.py)                        | Downloads data, Preprocess data by converting categorical columns to numeric, Standarizes numeric columns. | **No, unless** you want to add/remove parameters, or change parameter default values.

### Scripts

* [train-local.sh](scripts/train-local) This script trains a model locally. 
  It generates a SavedModel in local folder and verifies predictions locally.

* [train-cloud.sh](scripts/train-cloud.sh) This script submits a training job to AI Platform.

* [cloud-deploy-model.sh](scripts/cloud-deploy-model.sh) This script
  submits a model to AI Platform Prediction.

## How to run

Once the prerequisites are satisfied, you may:

1. For local training run:

```
source ./scripts/train-local.sh
```

2. For cloud training run:

```
source ./scripts/train-cloud.sh
```

3. For cloud deployment run:

```
source ./scripts/cloud-deploy-model.sh
```
## Custom prediction

We use two Python scripts for
[custom prediction](https://cloud.google.com/ai-platform/prediction/docs/custom-prediction-routine-keras)

```python
## Create a Preprocessor file

import pickle 
import preprocess

processor = preprocess.Preprocessor()

with open('./preprocessor.pkl', 'wb') as f:
    pickle.dump(processor, f)
```

### Versions
TensorFlow v2.1+
