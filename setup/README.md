# Setup your Environment

## Setup GCP

The best way to setup your GCP project is to use this section in this
[tutorial](https://cloud.google.com/ml-engine/docs/tensorflow/getting-started-training-prediction#set-up-your-gcp-project).

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

## Install Dependencies

Each sample folder has a `requirements.txt` file, containing all eh dependencies.
To run each sample, install the python dependencies using the following command:
 
 ```
pip install --upgrade -r requirements.txt
 ```
 
 ## Setup Environment Variables
 
Open `setup.sh` in this directory. Modify it and set `PEOJECT_ID` and `BUCKET_NAME` properly, before running it.
