# TensorFlow Estimator - Trainer Package

## Overview

The purpose of this directory is to provide a sample for how you can package a
TensorFlow training model to submit it to AI Platform. The sample makes it
easier to organise your code, and to adapt it to your dataset. In more details,
the template covers the following functionality:

*   Metadata to define your dataset, along with the problem type (Classification).
*   Standard implementation of input, parsing, and serving functions.
*   Automatic feature columns creation based on the metadata (and normalization stats).
*   Wide & Deep model construction using canned estimators.
*   Train, evaluate, and export the model.
*   Parameterization of the experiment.

Although this sample provides standard implementation to different
functionality, you can customise these parts with your own implementation.

## Prerequisites

* Follow the instructions in the *setup* directory in order to setup your environment
* Follow the instructions in the *datasets* directory to download the *Taxi Trips* dataset
* Create a Python virtual environment and run `pip install -r requirements.txt`

## Sample Structure

* `trainer` directory: with all the python modules to adapt to your data
* `scripts` directory: command-line scripts to train the model locally or on AI Platform
* `requirements.txt`: containing all the required python packages for this sample 
* `config.yaml`: for hyper-parameter tuning and specifying the AI Platform scale-tier

### Trainer Template Modules

File Name                                         | Purpose                                                                                                                                                                                                                                                                                                                                | Do You Need to Change?
:------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------
[metadata.py](trainer/metadata.py)     | Defines: 1) task type, 2) input data header, 3) numeric and categorical feature names, and 4) target feature name (and labels, for a classification task)                                                                                                                                                                              | **Yes**, as you will need to specify the metadata of your dataset. **This might be the only module to change!**
[inputs.py](trainer/inputs.py)         | Includes: 1) data input functions to read data from csv and tfrecords files, 2) parsing functions to convert csv and tf.example to tensors, 3) function to implement your custom features processing and creation functionality, and 4) prediction functions (for serving the model) that accepts CSV, JSON, and tf.example instances. | **Maybe**, if you want to implement any custom pre-processing and feature creation during reading data.
[featurizer.py](trainer/featurizer.py) | Creates: 1) TensorFlow feature_column(s) based on the dataset metadata (and other extended feature columns, e.g. bucketisation, crossing, embedding, etc.), and 2) deep and wide feature column lists.                                                                                                                                 | **Maybe**, if you want to change your feature_column(s) and/or change how deep and wide columns are defined.
[model.py](trainer/model.py)           | Includes: 1) function to create DNNLinearCombinedRegressor, and 2) DNNLinearCombinedClassifier.                                                                                                                                                                                                                                        | **No, unless** you want to change something in the estimator, e.g., activation functions, optimizers, etc..
[experiment.py](trainer/task.py)       | Runs the model training and evaluation experiment, and exports the final model.                                                                                                                                                                                                                                                        | **No, unless** you want to add/remove parameters, or change parameter default values.
[task.py](trainer/task.py)             | Includes: 1) Initialise and parse task arguments (hyper parameters), and 2) Entry point to the trainer.                                                                                                                                                                                                                                | **No, unless** you want to add/remove parameters, or change parameter default values.

### Scripts

* [train-local.sh](scripts/train-local) This script train a model locally. 
  It generates a Saved Model in local folder and verifies predictions locally.

* [train-ai-platform.sh](scripts/train-ai-platform.sh) This script submits a training job to AI Platform.

## How to run

Once the prerequisites are satisfied, you may:

    1. Run `source ./scripts/train-local.sh` for local training.
    2. Run `source ./scripts/train-cloud.sh` for cloud training.

### Version

Suitable for TensorFlow v1.13.1+
