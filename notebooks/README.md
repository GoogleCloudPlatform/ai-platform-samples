# AI Platform Notebooks

AI Platform Notebooks is a managed service that offers an integrated JupyterLab environment in which machine learning 
developers and data scientists can create instances running JupyterLab that come pre-installed with the latest data 
science and machine learning frameworks in a single click. Notebooks is integrated with BigQuery, Cloud Dataproc, and 
Cloud Dataflow, making it easy to go from data ingestion to preprocessing and exploration, and eventually model training 
and deployment.

# Tools

- [Notebooks auto-shutdown](tools/auto-shutdown): This script will
  continuously monitor the CPU load and will shut down the instance if
  the load is less than a particular threshold (for a specified amount
  of time). It also can check Docker CPU utilization and shut down the host VM
  as described above.
- [Notebook executor](tools/gcp-notebook-executor): 
This repository contains the logic that can be used to schedule Jupyter notebooks from anywhere (local, GCE, GCP Notebooks) to the [Google Cloud Deep Learning VM](https://cloud.google.com/deep-learning-vm/). You can read more about the usage of this tool [here](https://blog.kovalevskyi.com/gcp-notebook-executor-v0-1-2-8e37abd6fae1).
- [Notebook CI showcase](tools/notebooks-ci-showcase):
A fully functional continuous integration and continuous deployment system for Jupyter Notebooks.
- [Nova Agent](tools/nova-agents): Allows you to execute notebooks directly from your Jupyter UI. Nova and its corresponding compute 
workload runs on a separate Compute Engine instance using Nteract [papermill](https://github.com/nteract/papermill).
- [Nova Jupyterlab extensions](tools/nova-jupyterlab-extensions): Nova Plugin.
- [Notebook Deployment Manager](tools/deployment-manager): Automating AI Platform Notebook Instance Creation With GCP Deployment Manager.

# Templates

- [AI Platform Notebooks Template](templates/ai_platform_notebooks_template.ipynb)
- [AI Platform Notebooks/Colab Template](templates/ai_platform_notebooks_template_hybrid.ipynb)

# How to get help?

If you have further questions, or encounter issues using AI Platform Notebooks, 
open an issue or reach out at our team's forum: https://groups.google.com/forum/#!forum/google-dl-platform
