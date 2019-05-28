# TensorFlow Estimator - Trainer Package

## Overview

The purpose of this repository is to provide a sample of how you can package a
TensorFlow training model to submit it to AI Platform. The code makes it
easier to organise your code, and to adapt it to your dataset. In more details,
the template covers the following functionality:

*   Metadata to define your dataset, along with the problem type
    (Classification).
*   Standard implementation of input, parsing, and serving functions.
*   Automatic feature columns creation based on the metadata (and normalization
    stats).
*   Wide & Deep model construction using canned estimators.
*   Train, evaluate, and export the model.
*   Parameterization of the experiment.

Although this sample provides standard implementation to different
functionality, you can customise these parts with your own implementation.

### Setup your Google Cloud Platform environment

The best way to setup your GCP project is to use this section in this
[tutorial](https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction#set-up-your-gcp-project).

* **Environment setup:**

Virtual environments are strongly suggested, but not required. Installing this
sample's dependencies in a new virtual environment allows you to run the sample
locally without changing global python packages on your system.

There are two options for the virtual environments:

*   Install [Virtualenv](https://virtualenv.pypa.io/en/stable/) 
    *   Create virtual environment `virtualenv myvirtualenv`
    *   Activate env `source myvirtualenv/bin/activate`
*   Install [Miniconda](https://conda.io/miniconda.html)
    *   Create conda environment `conda create --name myvirtualenv python=3.5`
    *   Activate env `source activate myvirtualenv`

* **Install dependencies**

Install the python dependencies. `pip install --upgrade -r requirements.txt`



### Repository Structure

1.  **[core](core)** This directory includes: 
    - A trainer `trainer` folder with all the python modules to adapt to your data. 
    - A `setup.py` file for project configuration 
    - A `config.yaml` file for hyper-parameter tuning and specifying the AI Platform scale-tier.

2.  **[scripts](scripts)** This directory includes command-line scripts to:
    - Train the model locally. 
    - Download training data. 
    - Train the model on AI Platform.

The examples show how the template is adapted given a dataset. The datasets are
found in the examples' folders (under "data" sub-directory).

### Trainer Template Modules

File Name                                         | Purpose                                                                                                                                                                                                                                                                                                                                | Do You Need to Change?
:------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------
[metadata.py](trainer/metadata.py)     | Defines: 1) task type, 2) input data header, 3) numeric and categorical feature names, and 4) target feature name (and labels, for a classification task)                                                                                                                                                                              | **Yes**, as you will need to specify the metadata of your dataset. **This might be the only module to change!**
[inputs.py](trainer/inputs.py)         | Includes: 1) data input functions to read data from csv and tfrecords files, 2) parsing functions to convert csv and tf.example to tensors, 3) function to implement your custom features processing and creation functionality, and 4) prediction functions (for serving the model) that accepts CSV, JSON, and tf.example instances. | **Maybe**, if you want to implement any custom pre-processing and feature creation during reading data.
[featurizer.py](trainer/featurizer.py) | Creates: 1) TensorFlow feature_column(s) based on the dataset metadata (and other extended feature columns, e.g. bucketisation, crossing, embedding, etc.), and 2) deep and wide feature column lists.                                                                                                                                 | **Maybe**, if you want to change your feature_column(s) and/or change how deep and wide columns are defined.
[model.py](trainer/model.py)           | Includes: 1) function to create DNNLinearCombinedRegressor, and 2) DNNLinearCombinedClassifier.                                                                                                                                                                                                                                        | **No, unless** you want to change something in the estimator, e.g., activation functions, optimizers, etc..
[experiment.py](trainer/task.py)       | Runs the model training and evaluation experiment, and exports the final model.                                                                                                                                                                                                                                                        | **No, unless** you want to add/remove parameters, or change parameter default values.
[task.py](trainer/task.py)             | Includes: 1) Initialise and parse task arguments (hyper parameters), and 2) Entry point to the trainer.                                                                                                                                                                                                                                | **No, unless** you want to add/remove parameters, or change parameter default values.

## Scripts

  [aiplatform-deploy-model.sh](scripts/aiplatform-deploy-model.sh)  This script deploys a model in 
  AI platform Prediction. It expects a Saved Model in Google Cloud Storage.
  
  [download-data.sh](scripts/download-data.sh)  This script downloads data from Google Cloud Storage to
  a local directory. Run before [local-train.sh](scripts/aiplatform-deploy-model.sh)
  
  [local-train.sh](scripts/aiplatform-deploy-model.sh)  This script train a model locally. 
  It generates a Saved Model in local folder and verifies predictions locally.

## How to run

The following steps are required to run the following sample:

    1. Run `download-data.sh` script
    2. Run `local-train.sh` script for local training.
    3. Run `aiplatform-submit-train` for Cloud training.
  
## Dataset

Scripts will look for a data/ folder to contain, this dataset exists in `.download_data.sh` to
create folder and download files:

 - nano_taxi_trips_train.csv
 - nano_taxi_trips_eval.csv
 - new-data.json
 - new-data.csv
 

### Version

Suitable for TensorFlow v1.13.1+
