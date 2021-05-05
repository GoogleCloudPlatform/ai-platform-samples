# Google Cloud AI Platform Products

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

Welcome to the [AI Platform](https://cloud.google.com/ml-engine/docs/) sample code repository. This repository contains samples for how to use AI Platform products.

## Overview

The repository is organized by products: 

 - [AI Platform (Unified)](ai-platform-unified)   
 - [AI Platform Training](training)   
     - [Horovod](training/horovod)
     - [PyTorch](training/pytorch)
     - [scikit-learn](training/sklearn)
     - [TensorFlow](training/tensorflow)
     - [XGBoost](training/xgboost)
 - [AI Platform Prediction](prediction)
     - [scikit-learn](prediction/sklearn)
     - [TensorFlow](prediction/tensorflow)
     - [XGBoost](training/xgboost)
    - [Tools](prediction/tools) AI Platform Prediction tools 
 - [AI Platform Optimizer](notebooks/samples/optimizer)
 - [AI Platform Pipelines](pipelines)
 - [AI Platform Notebooks](notebooks)    
    - [Samples](notebooks/samples)
       - [AI Hub](notebooks/samples/aihub)       
       - [AI Platform Optimizer](notebooks/samples/optimizer)
       - [AI Platform Pipelines](notebooks/samples/tensorflow/sentiment_analysis)
       - [PyTorch](notebooks/samples/pytorch)
       - [TensorFlow](notebooks/samples/tensorflow)
    - [Templates](notebooks/templates) Templates used to contribute to AI Platform samples
    - [Tools](notebooks/tools) AI Platform Notebooks tools
 - [AI Hub](notebooks/samples/aihub)
 
 
<!--
 Commenting these out until we have at least a sample for them in the repo:
 - [Deep Learning VM Images](dlvm)
 - [Data Label Services](https://cloud.google.com/data-labeling/docs/)
 - [Built-in Algorithms](built_in_algorithms)
 -->

## Getting Started

We highly recommend that you start with our [Quick Start Sample](./quickstart).

## Navigating this Repository

This repository is organized based on the available products on AI Platform, and the typical Machine Learning problems 
that developers are trying to solve. For instance, if you are trying to train a model with [scikit-learn](https://scikit-learn.org), 
you will find the sample under [training/sklearn/structured/base](./training/sklearn/structured/base) directory.
AI Platform also supports [xgboost](https://xgboost.readthedocs.io/en/latest/), [TensorFlow](https://www.tensorflow.org), and [PyTorch](https://pytorch.org/).

Please refer to the `README.md` file in each sample directory for more specific instructions.


## Google Machine Learning Repositories

If you’re looking for our guides on how to do Machine Learning on Google Cloud Platform (GCP) using other services, please checkout our other repositories: 

- [ML on GCP](https://github.com/GoogleCloudPlatform/ml-on-gcp), which has guides on how to bring your code from various ML frameworks to [Google Cloud Platform](https://cloud.google.com/) using things like [Google Compute Engine](https://cloud.google.com/compute/) or [Kubernetes](https://kubernetes.io/).
- [Keras Idiomatic Programmer](https://github.com/GoogleCloudPlatform/keras-idiomatic-programmer) This repository contains content produced by Google Cloud AI Developer Relations for machine learning and artificial intelligence. The content covers a wide spectrum from educational, training, and research, covering from novices, junior/intermediate to advanced.
- [Professional Services](https://github.com/GoogleCloudPlatform/professional-services), common solutions and tools developed by Google Cloud's Professional Services team.

## Contributing a notebook

Only Googlers may contribute to this repo. If you are a Googler,  please see [go/cloudai-notebook-workflow](http://go/cloudai-notebook-workflow) for instructions.

## Troubleshooting

For common issues and solutions, please check our [troubleshooting](./TROUBLESHOOTING.md) page.

---

## Getting help

Please use the [issues page](https://github.com/GoogleCloudPlatform/ai-platform-samples/issues) to provide feedback or submit a bug report.

## Disclaimer
This is not an officially supported Google product. The code in this repository is for demonstrative purposes only.
