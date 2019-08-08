# AI Platform Training

The AI Platform training service allows you to train models using a wide range of different customization options.

You can use the following features:

 - Running a training job using many different machine types
 - Use GPUs
 - Use TPUs
 - Hyperparameter tuning
 - Distributed training

You can also select different ways to customize your training application. You can submit your input data for AI 
Platform to train using a [built-in algorithm (beta)](https://cloud.google.com/ml-engine/docs/algorithms/).
If the built-in algorithms do not fit your use case, you can submit your own training application to run on AI Platform, 
or build a [custom container (beta)](https://cloud.google.com/ml-engine/docs/custom-containers) with your training application and its dependencies to run on AI Platform.

ML Frameworks
-------------

This folder covers different functionality available in different frameworks:

 - [TensorFlow](https://www.tensorflow.org)
 - [scikit-learn](https://www.scikit-learn.org)
 - [XGBoost](https://github.com/dmlc/xgboost)
 - [PyTorch](https://www.pytorch.org)

Samples
-------------

This folder covers different functionality available AI Platform Training, the following samples reflect the available 
features in AI Platform:

#### AI Platform Training

The AI Platform training service allows you to train models using a wide range of different customization options.
You can select many different machine types to power your training jobs, enable distributed training, use hyperparameter 
tuning, and accelerate with GPUs and TPUs.

 - [TensorFlow](tensorflow/structured)
     - [Base](tensorflow/structured/base) Standard code to perform AI Platform Training using TensorFlow Estimators 
              using CPU.
     - [GPU](tensorflow/structured/gpu) Uses GPU and MirroredStrategy for Model Training.
     - [TPU](tensorflow/structured/tpu) Uses Cloud TPU for Model Training.
     - [Hyperparameter tuning](tensorflow/structured/hp_tuning) Use Hyperparameter tuning.
     - [Distributed training](tensorflow/structured/distributed) Uses Distributed Training using TensorFlow 
              Distribution strategy.
     
 - [scikit-learn](sklearn/structured/)
      - [Base](sklearn/structured/base) Standard code to perform AI Platform Training using Sci-kit learn 
              using CPU.
 - [XGBoost](xgboost/structured/)
      - [Base](xgboost/structured/base) Standard code to perform AI Platform Training using XGBoost. 
 
#### AI Platform Training - Custom Containers

Containers on AI Platform is a feature that allows you to run your application within a Docker image. You can build your own custom container to run jobs on AI Platform, using ML frameworks and versions as well as non-ML dependencies, libraries and binaries that are not otherwise supported on AI Platform.

 - [PyTorch](pytorch/structured)

#### AI Platform Prediction

 - [TensorFlow](tensorflow/structured)
 
**Note:** These examples use the [Chicago Taxi Trips Dataset](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew)
released by the City of Chicago. 
[Read more](https://cloud.google.com/bigquery/public-data/chicago-taxi) about the dataset in [Google BigQuery](https://cloud.google.com/bigquery/).


Templates
---------

* [TensorFlow Estimator Trainer Package Template](templates/tensorflow) - When training a Tensorflow model, you have to create a trainer package, here we have a template that simplifies creating a trainer package for AI Platform. Take a look at this list with some introductory [examples](tensorflow/ai-platform-template/examples/). 

* [Tensorflow: Cloud TPU Templates](templates/tensorflow/tpu) - A collection of minimal templates that can be run on Cloud TPUs on Compute Engine, AI Platform, and Colab.

* [Scikit-learn Pipelines Trainer Package Template](templates/sklearn) - You can use this as starter code to develop a scikit-learn model for training and prediction on AI Platform.

How to contribute?
------------------

We welcome external sample contributions! To learn more about contributing new samples, checkout our [CONTRIBUTING.md](CONTRIBUTING.md) guide. Please feel free to add new samples that are built in notebook form or code form with a README guide. 

Want to contribute but don't have an idea? Check out our [Sample Request Page](https://github.com/GoogleCloudPlatform/ai-platform-samples/issues?q=is%3Aissue+is%3Aopen+label%3ASAMPLE_REQUEST) and assign the issue to yourself so we know you're working on it!

Documentation
-------------

We host AI Platform documentation [here](https://cloud.google.com/ml-engine/docs/)
