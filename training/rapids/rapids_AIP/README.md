
## Scale model training from 10 GB to 640 GB training in minutes with RAPIDS + Dask and GPUs on AI Platform

**This example is not an officially supported Google product, does not have a SLA/SLO, and should not be used in production.**

This repository contains a tutorial for using Dask on GCP's AI Platform. It accompanies this blog post.


Python has solidified itself as one of the top languages for data scientists looking to prep, process, and analyze data for analytics and machine learning (ML) related use cases. However, Python can not scale on its own, creating major obstacles for data scientists seeking to deploy their code in production environments. Increasingly, ML tasks must process massive amounts of data, requiring the processing to be distributed across multiple virtual machines. Libraries like Dask and RAPIDS help data scientists manage that distributed processing. Google Cloud’s AI Platform enables data scientists to easily provision extremely powerful virtual machines with those libraries pre-installed, and a variety of speed-boosting GPU’s to boot. 

RAPIDS is a suite of open-source libraries that enable data scientists to leverage GPUs in their ML pipelines.

Dask is an open-source library for parallel computing in Python that helps data scientists scale their ML workloads.

AI Platform is Google Cloud’s fully-managed end-to-end platform that provides data scientists with automatically-provisioned environments and machines to do data science and  ML.

Put them together, and you can do scalable distributed training on a cluster of your specification, accelerated by GPUs. That is what we will be walking you through in this tutorial!

