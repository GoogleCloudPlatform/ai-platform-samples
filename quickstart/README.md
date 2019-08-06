# A short End-to-End Tutorial for AI Platform

## Overview

If this is your first time using [AI Platform](https://cloud.google.com/ml-engine/docs/),
we suggest you take a look at the [Introduction to AI Platform](https://cloud.google.com/ml-engine/docs/technical-overview) docs to have an understanding of the platform.

In this short tutorial, we will go over the basic steps for training a model
on AI Platform and using it for making predictions. We highly recommend that 
you go through this tutorial carefully as it illustrates many important steps which 
are essential in any training and/or prediction tasks on AI Platform.

In this tutorial, we will train a simple linear regression model with scikit-learn
using a dummy data. We will then deploy it to AI Platform and use it to make some
predictions. Finally we will delete the model from AI Platform and release all the used resources.

## Prerequisites

* Follow the instructions in the [setup](../setup) directory in order to setup your environment
* Create a Python 3 virtual environment and activate it
* Change the directory to this sample and run `python setup.py install`. Note: This 
is mostly for local testing of your code. When you submit a training job, no code will be
executed on your local machine. 

## Sample Structure

* [trainer](./trainer) directory: containing the training package to be submitted to AI Platform
  * [__init__py](./trainer/__init__.py) which is an empty file. It is needed to make this directory a Python package.
  * [task.py](./trainer/task.py) contains the training code. It create a simple dummy linear dataset
  and trains a linear regression model with scikit-learn and saves the trained model
  object in a directory (local or GCS) given by the user. 
* [scripts](./scripts) directory: command-line scripts to train the model locally or on AI Platform.
  We recommend to run the scripts in this directory in the following order, and use
  the `source` command to run them, in order to export the environment variables at each step:
  * [train-local.sh](./scripts/train-local.sh) trains the model locally using `gcloud`. It is always a
  good idea to try and train the model locally for debugging, before submitting it to AI Platform.
  * [train-cloud.sh](./scripts/train-cloud.sh) submits a training job to AI Platform.
  * [deploy.sh](./scripts/deploy.sh) creates a model resource, and a model version for the newly trained model.
  * [cleanup.sh](./scripts/cleanup.sh) deletes all the resources created in this tutorial.
* [prediction](./prediction) containing a Python sample code to invoke the model for prediction.
  * [predict.py](./prediction/predict.py) invokes the model for some predictions.
* [setup.py](./setup.py): containing all the required Python packages for this tutorial.


## Running the Sample

After you go over the steps in the prerequisites section, you are ready to run this sample.
Here are the steps you need to take:

1. _[Optional]_ Train the model locally. Run `source ./scripts/train-local.sh` as many times as
you like (This has no effect on your cloud usage). If successful, this script should
create a new model as `trained/quickstart/model.joblib`, which means you may now submit a
training job to AI Platform.

2. Submit a training job to AI Platform. Run `source ./scripts/train-cloud.sh` This will create a 
training job on AI Platform and displays some instructions on how to track the job progress.
At the end of a successful training job, it will upload the trained model object to a GCS
bucket and sets `$MODEL_DIR` environment variable to the directory containing the model.

3. Once the model object is created, you can deploy it for prediction. For that,
you'll need to create a model resource, and also a model version. A model resource is
like a container for one or more model versions. Run `source ./scripts/deploy.sh` which 
creates both the model resource and then the model version. _Note:_ If either the model
resource or the model version already exists, the script will display an error message.

4. Once the model is deployed, you may use it to make predictions. Simple, run 
`python ./prediction/predict.py`. This sample code sends a prediction request for two 
instances and prints the result to the console.

5. You may want to delete the resources you created in this tutorial. For that, simply 
run `source ./scripts/cleanup.sh` which deletes the model version and resouce, and also
the model object from GCS.

## Explaining Key Elements

In this section, we'll highlight the main elements of this sample.

### [task.py](./trainer/task.py)

In this sample we are not passing the input dataset as a parameter. However, we need
to save the trained model. To keep things simple, the code expects one argument
to be passed to the code: the path to to store the model in. In other examples, we will
be using `argparse` to process the input arguments. However, in this sample, we simply
read the input argument from `sys.argv[1]`.

Also note that we save the model as `model.joblib` which is
the name that AI Platform expects for models saved with `joblib` to have.

Finally, we are using `tf.gfile` from TensorFlow to upload the model to GCS. It does
not mean we are actually using TensorFlow in this sample to train a model. You may 
also use `google.cloud.storage` library for uploading and downloading to/from GCS.
The advantage of using `tf.gfile` is that it works seamlessly whether the file
path is local or a GCS bucket.

### [train-local.sh](./scripts/train-local.sh)

The command to run the training job locally is this:

```bash
gcloud ai-platform local train \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH} \
        -- \
        ${MODEL_DIR}
```

* `module-name` is the name of the Python file inside the package which runs the training job
* `package-path` determines where the training Python package is.
* `--` this is just a separator. Anyhing after this will be passed to the training job as input argument.
* `${MODEL_DIR}` will be passed to `task.py` as `sys.argv[1]`

### [train-cloud.sh](./scripts/train-cloud.sh)

To submit a training job to AI Platform, the main command is:

```bash
gcloud ai-platform jobs submit training ${JOB_NAME} \
        --job-dir=${MODEL_DIR} \
        --runtime-version=${RUNTIME_VERSION} \
        --region=${REGION} \
        --scale-tier=${TIER} \
        --module-name=trainer.task \
        --package-path=${PACKAGE_PATH}  \
        --python-version=${PYTHON_VERSION} \
        -- \
        ${MODEL_DIR}
```

* `${JOB_NAME}` is a unique name for each job. We create one with a timestamp to make it unique each time.
* `scale-tier` is to choose the tier. For this sample, we use BASIC. However, if you need
to use accelerators for instance, or do a distributed training, you will need a different tier. 
