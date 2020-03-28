## Streaming Analytics

### Google Cloud Machine Learning Pipeline.
#### Pub/Sub to AI Platform and then Google Cloud BigQuery

* [PubSubToBigQuery.py](PubSubToBigQuery.py)

The following example will run a streaming pipeline. It will read 
messages from a Pub/Sub topic, then window them into fixed-sized intervals, 
after that, it will call the Prediction API, once it gets the results,
will write them into BigQuery.

+ `--project`: sets the Google Cloud project ID to run the pipeline on
+ `--input-topic`: sets the input Pub/Sub topic to read messages from
+ `--region`: sets the region where Dataflow pipeline runs
+ `--staging-location`:  needed for executing the pipeline
+ `--temp-location`: needed for executing the pipeline
+ `--bigquery-dataset`:  BigQuery dataset reference
+ `--bigquery-table`: BigQuery table reference for output.
+ `--window-size [optional]`: specifies the window size in seconds, defaults to 60
+ `--min-batch-size [optional]`: specifies the batch min size
+ `--max-batch-size [optional]`: specifies the batch max size
+ `--runner`: specifies the runner to run the pipeline, if not set to `DataflowRunner`, `DirectRunner` is used

### Pre-requisites

### Streaming data

Run the [listener](../listener) example which gets Twitter streaming data
and pushes it to a PubSub topic.

### BigQuery 

1. Create a BigQuery dataset in BigQuery UI
2. Create BigQuery table using BigQuery UI

```postgres-sql
CREATE TABLE your_bq_dataset.your_bq_table (
    id STRING NOT NULL,
    text STRING,
    user_id STRING,
    sentiment FLOAT64,
    posted_at TIMESTAMP,
    favorite_count INT64,
    retweet_count INT64,
    media STRING
 )
 PARTITION BY DATE(_PARTITIONTIME)
 OPTIONS(
   description="A Twitter table"
 );
```

1. To test locally, define the DataFlow pipeline parameters via
   `set_env.sh`
  
```shell script
export PROJECT_ID=your_project # TODO Change
export MODEL_NAME=your_model_name # TODO Change
export INPUT_TOPIC=projects/$PROJECT_ID/topics/$TOPIC
export STAGING_LOCATION=gs://$BUCKET_NAME/dataflow-pipeline/staging
export TEMP_LOCATION=gs://$BUCKET_NAME/dataflow-pipeline/tmp
export REGION=us-central1
export BIGQUERY_DATASET=your_bq_dataset # TODO Change
export BIGQUERY_TABLE=your_bq_table # TODO Change
export WINDOW_SIZE=60
export MIN_BATCH_SIZE=5
export MAX_BATCH_SIZE=10
export RUNNER=DataflowRunner
```

Define your Credentials file:
```
export GOOGLE_CLOUD_CREDENTIALS='credentials.json'
```
Execute the program as follows:

```shell script
python PubSubToBigQueryWithAPI.py \
    --input-topic=${INPUT_TOPIC} \
    --region=${REGION} \
    --staging-location=${STAGING_LOCATION} \
    --temp-location=${TEMP_LOCATION} \
    --bigquery-dataset=${BIGQUERY_DATASET} \
    --bigquery-table=${BIGQUERY_TABLE} \
    --window-size=${WINDOW_SIZE} \
    --min-batch-size=${MIN_BATCH_SIZE} \
    --max-batch-size=${MAX_BATCH_SIZE} \
    --runner=${RUNNER} \
    --requirements_file requirements.txt &
```

## Docker

Build Docker container:

```shell script
docker build -t gcr.io/$PROJECT_ID/dataflow .
```

Create a `config.env` file:

```shell script
PROJECT_ID=
MODEL_NAME=sentiment_classifier
INPUT_TOPIC=projects/your_project/topics/news-ml-twitter
REGION=us-central1
STAGING_LOCATION=gs://BUCKET_NAME/news-ml-twitter/staging
TEMP_LOCATION=gs://BUCKET_NAME/news-ml-twitter/tmp
BIGQUERY_DATASET=your_dataset_twitter_test
BIGQUERY_TABLE=twitter_posts_test
GOOGLE_APPLICATION_CREDENTIALS=/config
RUNNER=DataflowRunner
WINDOW_SIZE=60
MIN_BATCH_SIZE=5
MAX_BATCH_SIZE=100

```

Start API

```shell script
docker run -d -itd --env-file=config.env \
 -v /keys/service-account.json:/config \
 gcr.io/$PROJECT_ID/dataflow:latest &
```
