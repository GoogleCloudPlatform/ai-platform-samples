# The Datasets

## Taxi Trips Dataset

The [Taxi Trips Dataset](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew) wasreleased by the City of Chicago.

Note: This site provides applications using data that has been modified
for use from its original source, www.cityofchicago.org, the official website of
the City of Chicago. The City of Chicago makes no claims as to the content,
accuracy, timeliness, or completeness of any of the data provided at this site.
The data provided at this site is subject to change at any time. It is
understood that the data provided at this site is being used at one’s own risk.

[Read more](https://cloud.google.com/bigquery/public-data/chicago-taxi) about
the dataset in [Google BigQuery](https://cloud.google.com/bigquery/). Explore
the full dataset in the
[BigQuery UI](https://bigquery.cloud.google.com/dataset/bigquery-public-data:chicago_taxi_trips).


The dataset in BigQuery is in a raw format. We have processed the dataset to prepare it for model training.

We have two different sizes of the dataset:

* Cloud: With 1M samples for training and 200K samples for evaluation
* Local: With 10K samples for local training and 2K samples for local evaluation

You can download either dataset (or both) by running one of the two following scripts:

```bash
# To download the both datasets:
source ./download-taxi.sh /path/to/output/directory

# To download the Cloud dataset only:
source ./download-taxi.sh /path/to/output/directory cloud

# To download the Local dataset only:
source ./download-taxi.sh /path/to/output/directory local
```

There are two additional files when you run the download script:

* [taxi_trips_prediction.txt](https://storage.cloud.google.com/cloud-samples-data/ml-engine/chicago_taxi/prediction/taxi_trips_prediction.txt): a header-less CSV file with 3 samples in a list, ready to be used for prediction
* [taxi_trips_prediction.json](https://storage.googleapis.com/cloud-samples-data/ml-engine/chicago_taxi/prediction/taxi_trips_prediction_list.json): a JSON file with 3 samples, ready to be used for prediction

The script also sets the following environment variables properly:

* [CLOUD_TAXI_TRAINING](https://storage.googleapis.com/cloud-samples-data/ml-engine/chicago_taxi/cloud/taxi_trips_train.csv): path to the Cloud training dataset
* [CLOUD_TAXI_EVALUATION](https://storage.googleapis.com/cloud-samples-data/ml-engine/chicago_taxi/cloud/taxi_trips_eval.csv): path to the Cloud evaluation dataset
* [LOCAL_TAXI_TRAINING](https://storage.googleapis.com/cloud-samples-data/ml-engine/chicago_taxi/local/taxi_trips_train.csv): path to the Local training dataset
* [LOCAL_TAXI_EVALUATION](https://storage.googleapis.com/cloud-samples-data/ml-engine/chicago_taxi/local/taxi_trips_eval.csv): path to the Local evaluation dataset

