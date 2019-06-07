# scikit-learn Estimator - Trainer Package

## Overview

The purpose of this directory is to provide a very short sample as a quick start
to train a model on AI Platform and use it for prediction. We highly recommend that 
you go through this sample carefully as it illustrates many important steps which 
are essential in any training and/or prediction tasks on AI Platform.tion.

In this sample we will train a very basic regression model using scikit-learn
using a dummy data. We will then deploy it to AI Platform and use it to make some
predictions. Finally we will delete the model from AI Platform and release all the used resources.

## Prerequisites

* Follow the instructions in the *setup* directory in order to setup your environment
* Create a Python virtual environment and run `pip install -r requirements.txt`

## Sample Structure

* `trainer` directory: containing the training package to be submitted to AI Platform
  * `task.py` contains the training code. It create a simple dummy linear dataset
  and trains a linear regression model with scikit-learn and saves the trained model
  object in a directory (local or GCS) given by the user. 
* `scripts` directory: command-line scripts to train the model locally or on AI Platform.
  We recommend to run the scripts in this directory in the following order,
  using `source ./XYZ.sh` where `XYZ` is the script name:
  * `train-local.sh` trains the model locally using `gcloud`. It is always a
  good idea to try and train the model locally for debugging, before submitting it to AI Platform.
  * `train-cloud.sh` submits a training job to AI Platform.
  * `deploy.sh` creates a model resource, and a model version for the newly trained model.
  * `cleanup` deletes all the resources created in this sample.
* `prediction` contains a python sample to invoke the model for prediction.
  * `predict.py` invokes the model for some predictions.
* `requirements.txt`: containing all the required python packages for this sample 


## Running the Sample

After you go over the steps in the prerequisites section, you are ready to run this sample.
Here are the steps you need to take:

1. [Optional] Train the model locally. Run `source ./scripts/train-local.sh` as many times as
you like (This has no effect on your cloud usage). If successful, this script should
create a new model as `trained/quickstart/model.joblib`, and you may now submit a
training job to AI Platform.

2. Submit a training job to AI Platform. Run `source ./scripts/train-cloud.sh` This will create a 
training job on AI Platform and displays some instructions on how to track the job progress.
At the end of a successful training job, it will uplaod the trained model object to a GCS
bucket and sets `$MODEL_DIR` environment variable to the directory containing the model.

3- Once the model object is created, you can deploy it for prediction. For that,
you'll need to create a model resource, and also a model version. A model resource is
like a container for one or more model versions. Run `source ./scripts/deploy.sh` which 
creates both the model resource and then the model version.

4- Once the model is deployed, you may use it to make predictions. Simple, call 
`python ./prediction/predict.py`. This sample code sends a prediction request for two 
instances and prints the result to the console.

5- You may want to delete the resources you created in this tutorial. For that, simply 
run `source ./scripts/cleanup.sh` which deletes the model version and resouce, and also
the model object from GCS.