# Setup your Environment

## Setup GCP

Before you can run any of the samples in this repository, you'll need to setup your GCP account and environment.
The main steps are:

1. Have a GCP account and create/select a GCP project on [GCP Console](https://console.cloud.google.com).

2. Enable the billing for your GCP project. Click [here](https://cloud.google.com/billing/docs/how-to/modify-project) for more information.

3. Download and install [Google Cloud SDK](https://cloud.google.com/sdk/docs/).

4. Configure the SDK by running `gcloud init` and following the instructions.

5. Enable the API for the following services:

  * [Compute Engine](https://pantheon.corp.google.com/compute). Run `gcloud services enable compute.googleapis.com`.
  * [Storage](https://pantheon.corp.google.com/storage). Run `gcloud services enable storage-component.googleapis.com`.
  * [AI Platform](https://pantheon.corp.google.com/mlengine). Run `gcloud services enable ml.googleapis.com`.

6. Create and download a service account key with the right permissions, by following the instructions [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-gcloud).

7. Open `setup.sh` in this directory. Set:
  - `PROJECT_ID`
  - `BUCKET_NAME` 
  - `GOOGLE_APPLICATION_CREDENTIALS` 
 
  Then run 
 
 ```bash
 source ./setup.sh
 ```

  
## Setup Virtual Environment

Virtual environments are strongly suggested, but not required. Installing this
sample's dependencies in a new virtual environment allows you to run the sample
locally without changing global python packages on your system.

There are two options for the virtual environments:

*   Install [Virtualenv](https://virtualenv.pypa.io/en/stable/) 
    *   Create virtual environment `virtualenv myvirtualenv`
    *   Activate env `source myvirtualenv/bin/activate`
*   Install [Miniconda](https://conda.io/miniconda.html)
    *   Create conda environment `conda create --name myvirtualenv python=3.5`
    *   Activate env `source activate myvirtualenv`
    
## 

## Install Dependencies

Each sample folder has a `setup.py` file, containing all the dependencies.
To run each sample, install the python dependencies using the following command:
 
 ```
python setup.py install
 ```
 
