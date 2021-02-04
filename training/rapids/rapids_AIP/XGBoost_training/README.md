## Submit AI Platform Training job using custom container
## First, you must update build.sh, rapids_distributed.yaml

'''This example is not an officially supported Google product, does not have a SLA/SLO, and should not be used in production.'''

#bash build.sh

### Region must be central for A100s. Other GPUs are more flexible
export REGION=us-central1 
export JOB_NAME=rapids_job_$(date +%Y%m%d_%H%M%S)

gcloud ai-platform jobs submit training $JOB_NAME --region $REGION --config rapids_a100.yaml

#gcloud ai-platform jobs stream-logs $JOB_NAME