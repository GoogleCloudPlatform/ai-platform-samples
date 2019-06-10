# AI Platform Training

The AI Platform training service allows you to train models using a wide range of different customization options.

You can select many different machine types to power your training jobs, enable distributed training, use hyperparameter 
tuning, and accelerate with GPUs and TPUs.

You can also select different ways to customize your training application. You can submit your input data for AI 
Platform to train using a built-in algorithm (beta).
If the built-in algorithms do not fit your use case, you can submit your own training application to run on AI Platform, 
or build a custom container (beta) with your training application and its dependencies to run on AI Platform.

This folder covers different functionality available in different frameworks:

 - Running a training job
 - Distributed training
 - Using GPUs
 - Using TPUs
 - Hyperparameter tuning


Templates
---------

* [TensorFlow Estimator Trainer Package Template](tensorflow/template) - When training a Tensorflow model, you have to create a trainer package, here we have a template that simplifies creating a trainer package for AI Platform. Take a look at this list with some introductory [examples](cloudml-template/examples/). 

* [Tensorflow: Cloud TPU Templates](tpu/templates) - A collection of minimal templates that can be run on Cloud TPUs on Compute Engine, Cloud Machine Learning, and Colab.

* [Scikit-learn Pipelines Trainer Package Template](scikit-learn/template) - You can use this as starter code to develop a scikit-learn model for training and prediction on AI Platform. [Examples](scikit-learn/template/examples) to be added.

How to contribute?
------------------

We welcome external sample contributions! To learn more about contributing new samples, checkout our [CONTRIBUTING.md](CONTRIBUTING.md) guide. Please feel free to add new samples that are built in notebook form or code form with a README guide. 

Want to contribute but don't have an idea? Check out our [Sample Request Page](https://github.com/GoogleCloudPlatform/cloudml-samples/issues?q=is%3Aissue+is%3Aopen+label%3ASAMPLE_REQUEST) and assign the issue to yourself so we know you're working on it!

Documentation
-------------

We host AI Platform documentation [here](https://cloud.google.com/ml-engine/docs/)
