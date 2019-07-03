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

6. Create and download a service account key.
A [service account](https://cloud.google.com/iam/docs/service-accounts) is a special Google account that belongs to your application or a virtual machine (VM), instead of to an individual end user.

In order to create a service account key, you may follow the instructions [here](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#iam-service-account-keys-create-gcloud).
Alternatively, you may run this in your terminal, after setting the values for the 3 environment variables:


```bash
# A name for the service account you are about to create:
export SERVICE_ACCOUNT_NAME=your-service-account-name

# Your GCP project ID:
export PROJECT_ID=your-gcp-project-id

# The path where the service account json key should be saved to:
export GOOGLE_APPLICATION_CREDENTIALS=path/to/service/account/key

#Creathe service account:
gcloud iam service-accounts create ${MY_SERVICE_ACCOUNT} --display-name="Service Account for ai-platform-samples repo"

# Grant the required roles:
gcloud projects add-iam-policy-binding endromodal --member serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com --role roles/ml.developer
gcloud projects add-iam-policy-binding endromodal --member serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com --role roles/storage.objectAdmin

# Download the service account key:
gcloud iam service-accounts keys create ${GOOGLE_APPLICATION_CREDENTIALS} --iam-account ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com
```

7. Set and export the required environment variables. The samples in this repository rely on a 
number of environment variables to run properly. You may have already set `PROJECT_ID` and `GOOGLE_APPLICATION_CREDENTIALS`
in the previous step. [setup.sh](./setup.sh) sets and exports these required variables for you.

In your terminal, and from the root directory of the repository, run:

```bash
source ./setup/setup.sh
```

If an environment variable (e.g. `BUCKET_NAME`) has not been set properly, this script will show an error message. 
You may modify `setup.sh` to set the environment variable or simply use the `export` command in your terminal to set it.
You may run `setup.sh` as many times as you wish.

  
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
    

## Install Dependencies

Each sample folder has a `setup.py` file, containing all the dependencies.
To run each sample, install the python dependencies using the following command:
 
 ```bash
python setup.py install
 ```
 
