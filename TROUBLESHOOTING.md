# Troubleshooting

In this page, we will address some common issues that the developers often face while working with AI Platform samples and provide solutions.

## Potential Issues

### Issue: `gcloud` commands are not working properly

* Run `gcloud init` in your terminal and follow the instructions.
* Run `gcloud compute instances list` to make sure the API for Compute is enabled.
* Run `gcloud ai-platform models list` to make sure the API for AI Platform is enabled.
* Run `gsutil ls gs://` to make sure you have access to GCS.
* Run `gcloud info` to get more information about your configuration.

### Issue: Training job is failing

* Make sure you have followed the [setup steps](./setup).
    * Verify that the APIs are enabled.
    * Verify that the environment variables are set correctly.
* Confirm that `GOOGLE_APPLICATION_CREDENTIALS` is pointing to the correct service account key file for your GCP project.
Also, make sure the ervice account file is for your current GCP project and that it has the right roles, as specified in the setup page.
* Run `gcloud config list` and verify the account and the project are set correctly.


### Issue: Got a `Bad magic number in .pyc file` during local prediction

This is a known issue which occurs when you are using Python 3. It will be fixed in upcoming releases.
