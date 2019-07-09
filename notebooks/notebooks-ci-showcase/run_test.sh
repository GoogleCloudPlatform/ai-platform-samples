#!/bin/bash -u

# Sourcing logic that contains execute_notebook CLI
# This CLI is used to schedule notebooks
# To learn more:
# * original repository: https://github.com/gclouduniverse/gcp-notebook-executor
# * article about it: https://blog.kovalevskyi.com/how-to-submit-jupyter-notebook-for-overnight-training-on-gcp-4ce1b0cd4d0d
source gcp-notebook-executor/utils.sh

# Input values for the test, we only need 2:
# * Notebook that we are going to test
# * GCS location that is used during background training
# NOTE: your Cloud Build service account should have R/W access to GCS bucket. 
INPUT_NOTEBOOK="demo.ipynb"
GCS_LOCATION="gs://dl-platform-temp/notebook-ci-showcase"

# In our demo notebook we are using an API_KEY environment variable, this is only specific for our demo
# and very likely will not be needed in your case. Next line removes the new line at the end of the variable
# before passing it to the actual execution.
API_KEY=`echo "${API_KEY}"`

# execute_notebook will return 0 or 1 depends on the status of the notebook.
execute_notebook -i "./${INPUT_NOTEBOOK}" -o "${GCS_LOCATION}" -m "api_key=${API_KEY}" -g t4 -c 1
