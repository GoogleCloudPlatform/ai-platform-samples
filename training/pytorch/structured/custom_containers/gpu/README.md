# PyTorch Custom Containers GPU Template

## Overview

The purpose of this directory is to provide a sample for how you can package a
PyTorch training model to submit it to AI Platform. The sample makes it
easier to organise your code, and to adapt it to your dataset. In more details,
the template covers the following functionality:

*   Metadata to define your dataset, along with the problem type (Classification).
*   Standard implementation of input, parsing, and serving functions.
*   Automatic feature columns creation based on the metadata (and normalization stats).
*   Train, evaluate, and export the model.
*   Parameterization of the experiment.

Although this sample provides standard implementation to different
functionality, you can customise these parts with your own implementation.

## Prerequisites

* Setup your project by following the instructions in the [setup](../../../../setup/) directory.
* [Setup docker with Cloud Container Registry](https://cloud.google.com/container-registry/docs/pushing-and-pulling)
* The datasets are downloaded by the Dockerfile.
    * [OPTIONAL] The Dockerfile defaults to downloading the small dataset, if you wish to modify this, you can set which files to download via the `--build-arg` flag:
    ```
    docker build -f Dockerfile -t gcr.io/[PROJECT_ID]/pytorch_taxi_container:taxi_pytorch ./ \
       --build-arg train-files=gs://cloud-samples-data/ml-engine/chicago_taxi/training/small/taxi_trips_train.csv \
       --build-arg eval-files=gs://cloud-samples-data/ml-engine/chicago_taxi/training/small/taxi_trips_eval.csv
    ```
 * [OPTIONAL] Download the datasets using run [download-taxi.sh](../../../../datasets/download-taxi.sh) located in [datasets](../../../../datasets) folder.
* Change the directory to this sample and run


`Note:` These instructions are used for local testing. When you submit a training job, no code will be executed on your local machine.
  

## Sample Structure

* `trainer` directory: with all the python modules to adapt to your data
* `scripts` directory: command-line scripts to train the model locally or on AI Platform
* `Dockerfile`: define the docker image

### Trainer Template Modules

File Name                                         | Purpose                                                                                                                                                                                                                                                                                                                                | Do You Need to Change?
:------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------
[Dockerfile](Dockerfile)       | Defines the base docker image, installs the necessary libraries, downloads the dataset, and copies over the python training files | **Maybe**, as you may need to adjust which libaries are installed or specify the datasets your image should download.
[metadata.py](trainer/metadata.py)     | Defines: 1) task type, 2) input data header, 3) numeric and categorical feature names, and 4) target feature name (and labels, for a classification task)                                                                                                                                                                              | **Yes**, as you will need to specify the metadata of your dataset. **This might be the only module to change!**
[inputs.py](trainer/inputs.py)         | Includes: 1) data input functions to read data from csv files, 2) parsing functions to convert csv to tensors, 3) function to implement your custom features processing and creation functionality, and 4) prediction functions (for serving the model) that accepts CSV, JSON, and tf.example instances. | **Maybe**, if you want to implement any custom pre-processing and feature creation during reading data.
[model.py](trainer/model.py)           | Includes: 1) function to create DNNLinearCombinedRegressor, and 2) DNNLinearCombinedClassifier.                                                                                                                                                                                                                                        | **Yes** you want to cutomize the model to your inputs, the loss function, and the optimizer function.
[experiment.py](trainer/experiment.py)       | Runs the model training and evaluation experiment, and exports the final model.                                                                                                                                                                                                                                                        | **No, unless** you want to add/remove parameters, or change parameter default values.
[task.py](trainer/task.py)             | Includes: 1) Initialise and parse task arguments (hyper parameters), and 2) Entry point to the trainer.                                                                                                                                                                                                                                | **No, unless** you want to add/remove parameters, or change parameter default values.

### Scripts

* [train-local.sh](scripts/train-local) This script trains a model locally. 
  It generates a SavedModel in local folder on the Docker Image.

* [train-cloud.sh](scripts/train-cloud.sh) This script submits a training job to AI Platform.

## How to run

Once the prerequisites are satisfied, you may:

1. For local testing, run: (Note: if you don't have a GPU, the program will be run on the CPU)
    ```
    source ./scripts/train-local.sh
    ```
2. For cloud testing, run:
    ```
    source ./scripts/train-cloud.sh
    ```

## What's different from the base (cpu) template?
Not a lot changes when switching from a CPU to a GPU. Only a few lines are added / modified to make this possible. 

* `trainer/experiment.py`
   * Lines 99-104: Determine if a GPU device is availbe and set the `device` variable to CPU or GPU
   * Lines 109 & 112: Pass the device information to the data loading and model creation methods.
* `trainer/inputs.py`
   * Line 80: `device` is added as a method parameter
   * Lines 87-88: Pass the device information to the `CSVDataset` class
   * Lines 29 & 44: Accept and set the `device` in the `CSVDataset` class
   * Lines 70-71: Send the feature & target tensors to the device
* `trainer/model.py`
   * Line 39: `device` is added as a method parameter
   * Line 46: sends the DNN to the device

### Versions
PyTorch 1.0.0+
