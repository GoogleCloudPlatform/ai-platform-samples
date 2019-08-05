# Online Prediction with scikit-learn

## Overview

In this sample, we go over the steps to deploy a model trained with scikit-learn to AI-Platform.
We will then use the deployed model to make some predictions.
Optionally, we will delete the resources created in this sample.

## Prerequisites

* Complete [this training sample](../../../../training/sklearn/structured/base).
* Change the directory to this sample and run `python setup.py install`.

## Sample Structure

* [scripts](./scripts) directory: command-line scripts to train the model locally or on AI Platform.
  * [deploy.sh](./scripts/deploy.sh) creates a model resource, and a model version for the newly trained model.
  * [cleanup.sh](./scripts/cleanup.sh) deletes all the resources created in this tutorial.
* [prediction](./prediction) containing a Python sample code to invoke the model for prediction.
  * [predict.py](./prediction/predict.py) invokes the model for some predictions.
* [setup.py](./setup.py): containing all the required Python packages for this tutorial.


## Running the Sample

After you go over the steps in the prerequisites section, you are ready to run this sample.
Here are the steps you need to take:

1. Run `source ./scripts/deploy.sh`. This script will create a Model Resource in AI-Platform.
It will then deploy the model object which was created in the training sample as a new model
with an assigned model version.

2. Once the model is deployed, you may use it to make predictions. Simple, run 
`python ./prediction/predict.py`. This sample code sends a prediction request for two 
instances and prints the result to the console.

3. You may want to delete the resources you created in this tutorial. For that, simply 
run `source ./scripts/cleanup.sh` which deletes the model version and resouce, and also
the model object from GCS.


