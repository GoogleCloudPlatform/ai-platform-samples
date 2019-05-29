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


The dataset in BigQuery is in a raw format. We have processed the dataset a little to prepare it for model training. 

We have two different sizes of the dataset:

* Big: With 1M samples for training and 200K samples for evaluation
* Small: With 10K samples for training and 2K samples for evaluation

You can download either dataset (or both) by running one of the two following scripts (please use an absolute path for the output directory):
```bash
# To download the both datasets:
source ./download-taxi-big.sh /absolute/path/to/output/directory

# To download the big dataset only:
source ./download-taxi-big.sh /absolute/path/to/output/directory big

# To download the small dataset only:
source ./download-taxi-big.sh /absolute/path/to/output/directory small
```

There are two additional files when you run the download script::

* taxi_trips_prediction.csv: a header-less CSV file with 3 samples, ready to be used for prediction
* taxi_trips_prediction.json: a JSON file with 3 samples, ready to be used for prediction

The script also sets the following environment variables properly:

* BIG_TAXI_TRAINING: Path to the big training file
* BIG_TAXI_EVALUATION: Path to the big evaluation file
* SMALL_TAXI_TRAINING: Path to the small training file
* SMALL_TAXI_EVALUATION: Path to the small evaluation file

