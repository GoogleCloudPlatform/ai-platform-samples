# AI Platform Training

The AI Platform training service allows you to train models using a wide range of different customization options.

You can use the following features:

 - Running a training job using many different machine types
 - Use GPUs
 - Use TPUs
 - Hyperparameter tuning
 - Distributed training

You can also select different ways to customize your training application. You can submit your input data for AI 
Platform to train using a built-in algorithm (beta).
If the built-in algorithms do not fit your use case, you can submit your own training application to run on AI Platform, 
or build a custom container (beta) with your training application and its dependencies to run on AI Platform.

ML Frameworks
-------------

This folder covers different functionality available in different frameworks:

 - [TensorFlow](www.tensorflow.org)
 - [scikit-learn](www.scikit-learn.org)
 - [XGBoost](https://github.com/dmlc/xgboost)
 - [PyTorch](www.pytorch.org)

Samples
-------------

This folder covers different functionality available AI Platform Training:

### Structured data
 
This example uses the [Chicago Taxi Trips Dataset](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew)
released by the City of Chicago. 
[Read more](https://cloud.google.com/bigquery/public-data/chicago-taxi) about the dataset in [Google BigQuery](https://cloud.google.com/bigquery/).

The following samples reflect the available features in AI Platform:

#### Standard AI Platform Training

 - [TensorFlow](structured/tensorflow)
     - [CPU](structured/tensorflow/base) Standard configuration to perform AI Platform Training using TensorFlow Estimators
     - [GPU](structured/tensorflow/gpu) Uses GPU for AI Platform Training
     - [TPU](structured/tensorflow/tpu) Uses Cloud TPU for AI Platform Training
     - [Hyperparameter tuning](structured/tensorflow/hp_tuning) Use Hyperparameter Tuning
     - [Distributed training](structured/tensorflow/distributed) Uses Distrubuted Training using TensorFlow Distribution strategy
     
 - [scikit-learn](structured/scikit-learn)
 - [XGBoost](structured/xgboost)
 
#### Custom containers

 - [PyTorch](structured/pytorch)

Templates
---------

* [TensorFlow Estimator Trainer Package Template](tensorflow/template) - When training a Tensorflow model, you have to create a trainer package, here we have a template that simplifies creating a trainer package for AI Platform. Take a look at this list with some introductory [examples](cloudml-template/examples/). 

* [Tensorflow: Cloud TPU Templates](tpu/templates) - A collection of minimal templates that can be run on Cloud TPUs on Compute Engine, AI Platform, and Colab.

* [Scikit-learn Pipelines Trainer Package Template](scikit-learn/template) - You can use this as starter code to develop a scikit-learn model for training and prediction on AI Platform. [Examples](scikit-learn/template/examples) to be added.

How to contribute?
------------------

We welcome external sample contributions! To learn more about contributing new samples, checkout our [CONTRIBUTING.md](CONTRIBUTING.md) guide. Please feel free to add new samples that are built in notebook form or code form with a README guide. 

Want to contribute but don't have an idea? Check out our [Sample Request Page](https://github.com/GoogleCloudPlatform/ai-platform-samples/issues?q=is%3Aissue+is%3Aopen+label%3ASAMPLE_REQUEST) and assign the issue to yourself so we know you're working on it!

Documentation
-------------

We host AI Platform documentation [here](https://cloud.google.com/ml-engine/docs/)
