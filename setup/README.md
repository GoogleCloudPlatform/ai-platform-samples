# Setup your Environment

## Setup GCP

Before you can run any of the samples in this repository, you'll need to setup your GCP account and environment.
The main steps are:

1. Have a GCP account and create/select a GCP project on [GCP Console](https://console.cloud.google.com).

2. Enable the billing for your GCP project. Click [here](https://cloud.google.com/billing/docs/how-to/modify-project) for more information.

3. Download and install [Google Cloud SDK](https://cloud.google.com/sdk/docs/).

4. Configure the SDK by running:

From your terminal:

   ```shell
   gcloud init
   ```
   
   and follow the instructions.

5. Enable the API for the following services:

  * [Compute Engine](https://pantheon.corp.google.com/compute).
  * [Storage](https://pantheon.corp.google.com/storage).
  * [AI Platform](https://pantheon.corp.google.com/mlengine).

From your terminal:

```bash
gcloud services enable compute.googleapis.com
gcloud services enable storage-component.googleapis.com
gcloud services enable ml.googleapis.com
```

6. Create and download a service account key with the right permissions, follow the instructions [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-gcloud).

7. Export Environment variables for your Project:
 
From your terminal choose from the following two options:

a) Edit `setup.sh` in this directory. Set the following variables:
    
   - `PROJECT_ID`
   - `BUCKET_NAME` 
   - `GOOGLE_APPLICATION_CREDENTIALS` 
    
   Use `source` command to export them:
  
   ```bash
     source ./setup.sh
   ```

b) In your terminal copy and paste the following with the corresponding edits.

```bash
export RUNTIME_VERSION=1.13
export PYTHON_VERSION=3.5
export REGION=us-central1

# Replace "your-gcp-project-id" with your GCP PROJECT ID
export PROJECT_ID="your-gcp-project-id"

# Replace "your-gcp-bucket-name" with a universally unique name for a GCS bucket.
export BUCKET_NAME="your-gcp-bucket-name"

# Replace "path/to/service/account/key" with the full path to the
# service account key file which you created and downloaded.
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service/account/key"
```
  
## Setup your Virtual Environment

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
 
 ```bash
python setup.py install
 ```
 
