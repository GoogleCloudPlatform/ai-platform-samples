# main.py is the source for a cloud function, which when activated will send 
# a request to Cloud Build with an end date defined by the incoming message.
from datetime import timedelta
from dateutil import parser
import json
import yaml

from google.auth import compute_engine
import googleapiclient.discovery

# Create Cloud Build client with default credentials, credentials can be sourced in
# this way because Cloud Functions runs on Compute Engine.
credentials = compute_engine.Credentials()
build_client = googleapiclient.discovery.build('cloudbuild', 'v1', credentials=credentials)

# Loads deploy.yaml, adds the 'live' tested version of the notebook + executor code as
# the source. When Cloud Build runs, the archive will be extracted into the root of the
# build workspace.
with open("deploy.yaml", "r") as f:
    base_deploy_request = yaml.load(f)
base_deploy_request["source"] = {
    "storageSource": {
        "bucket": "dl-platform-temp",
        "object": "notebook-ci-showcase/live.tar.gz",
    }
}

# Run each time a message is received by the deployed Cloud Function.
# data is a json payload containing the event data, in this case it is expected to either be
# {} or {'today': 'YYYY-MM-DD'}. context contains metadata about execution.
# See https://cloud.google.com/functions/docs/writing/background#functions_background_parameters-python
def startrun(data, context):
    deploy_request = base_deploy_request.copy()
    
    if data and "today" in data:
        # "today" specified in cloud function invocation, use defined date
        today = parser.parse(data["today"])
    else:
        # dataset does not have current information, use last year's info (example dataset only reaches ~April 2018)
        today = parser.parse(context.timestamp) - timedelta(days=365)

    # Generating weekly reports
    one_week_ago = today - timedelta(days=7)
    
    # Overrides substitution fields in deploy.yaml
    deploy_request["substitutions"]["_START_DATE"] = "{:%Y-%m-%d}".format(one_week_ago)
    deploy_request["substitutions"]["_END_DATE"] = "{:%Y-%m-%d}".format(today)
    
    # Sends updated deploy.yaml to Cloud Build
    response = build_client.projects().builds().create(projectId="deeplearning-platform", body=deploy_request).execute()
    # returns OK or error queueing job
    return str(response)
