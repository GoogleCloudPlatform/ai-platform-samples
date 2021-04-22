# AI Platform Training

The AI Platform training service allows you to train models using a wide range of different customization options.

You can use the following features:

 - Running a training job using many different machine types
 - Use custom Docker containers with your preferred ML Framework
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
 - [Horovod](https://github.com/horovod/horovod)

Samples
-------------

This folder covers different functionality available AI Platform Training, the following samples reflect the available 
features in AI Platform:

#### AI Platform Training

The AI Platform training service allows you to train models using a wide range of different customization options.
You can select many different machine types to power your training jobs, enable distributed training, use hyperparameter 
tuning, and accelerate with GPUs and TPUs.

 - [TensorFlow](tensorflow/structured)
     - [base](tensorflow/structured/base) Standard code to perform AI Platform Training using TensorFlow Estimators 
              using CPU.
     - [census TF Keras](tensorflow/census/tf-keras) A Binary classification model using with TF Keras and AI Platform Trainining.
     - [TPU](tensorflow/structured/tpu) Uses Cloud TPU for Model Training.
     - [Hyperparameter tuning](tensorflow/structured/hp_tuning) Use Hyperparameter tuning.
     - [Distributed training](tensorflow/structured/distributed) Uses Distributed Training using TensorFlow 
              Distribution strategy.
     
 - [scikit-learn](sklearn/structured/)
      - [base](sklearn/structured/base) Standard code to perform AI Platform Training using Sci-kit learn 
              using CPU.
 - [XGBoost](xgboost/structured/)
      - [base](xgboost/structured/base) Standard code to perform AI Platform Training using XGBoost. 
 
 - [PyTorch](pytorch/)
     - [Text Classification](pytorch/text/sentiment_classification) PyTorch based text classification model by fine tuning a pre-trained Huggingface Transformers model on AI Platform Training
 
#### AI Platform Training - Custom Containers

Containers on AI Platform is a feature that allows you to run your application within a Docker image. You can build your own custom container to run jobs on AI Platform, using ML frameworks and versions as well as non-ML dependencies, libraries and binaries that are not otherwise supported on AI Platform.

 - [PyTorch](pytorch/structured) Train a PyTorch model in AI Platform
 - [Horovod](horovod) How to run Horovod on AI Platform.
 - [ResNet](tensorflow/custom_containers/hypertune) How to run custom containers using Hyperparameter tuning.

#### AI Platform Prediction

 - [TensorFlow](../prediction/tensorflow/structured)
 - [scikit-learn](../prediction/sklearn/structured/base)
 - [XGboost](../prediction/xgboost/structured/base)
 
**Note:** These examples use the [Chicago Taxi Trips Dataset](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew)
released by the City of Chicago. 
[Read more](https://cloud.google.com/bigquery/public-data/chicago-taxi) about the dataset in [Google BigQuery](https://cloud.google.com/bigquery/).


Templates
---------

* [Tensorflow: Cloud TPU Templates](templates/tensorflow/tpu) - A collection of minimal templates that can be run on Cloud TPUs on Compute Engine, AI Platform, and Colab.


How to contribute?
------------------

We welcome external sample contributions! To learn more about contributing new samples, checkout our [CONTRIBUTING.md](CONTRIBUTING.md) guide. Please feel free to add new samples that are built in notebook form or code form with a README guide. 

Want to contribute but don't have an idea? Check out our [Sample Request Page](https://github.com/GoogleCloudPlatform/ai-platform-samples/issues?q=is%3Aissue+is%3Aopen+label%3ASAMPLE_REQUEST) and assign the issue to yourself so we know you're working on it!

Documentation
-------------

We host AI Platform documentation [here](https://cloud.google.com/ml-engine/docs/)
