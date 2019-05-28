# AI Platform training

The AI Platform training service allows you to train models using a wide range of different customization options.

You can select many different machine types to power your training jobs, enable distributed training, use hyperparameter 
tuning, and accelerate with GPUs and TPUs.

You can also select different ways to customize your training application. You can submit your input data for AI 
Platform to train using a built-in algorithm (beta).
If the built-in algorithms do not fit your use case, you can submit your own training application to run on AI Platform, 
or build a custom container (beta) with your training application and its dependencies to run on AI Platform.

This folder covers different functionality available in different frameworks:

 - Running a training job
 - Distributed training
 - Using GPUs
 - Using TPUs
 - Hyperparameter tuning
 
### Dataset

AI Platform Samples Dataset

Dataset location:
Location: gs://cloud-samples-data/ml-engine/chicago_taxi/

Training and evaluation dataset:

##### Cloud training
   - 1M records 
   - Training 800K Eval: 200K
   Used for Google Cloud training and evaluation
   How it was created? SQL query below
        - mini_taxi_trips.csv
        - mini_taxi_trips_no_header.csv
        - mini_taxi_trips_train.csv
        - mini_taxi_trips_eval.csv
    * Train and evaluation files contain header

##### Local training dataset Chicago Taxi:
   - 100K records
   - Training 80K Eval: 20K	
   Used for local training and evaluation
   How it was created? SQL query below with a different LIMIT value.
        - nano_taxi_trips.csv
        - nano_taxi_trips_no_header.csv
        - nano_taxi_trips_train.csv
        - nano_taxi_trips_eval.csv
    * Train and evaluation files contain header

##### Prediction
   - new-data.json
   - new-data.csv

SQL creation

This query was executed using [BigQuery](https://cloud.google.com/bigquery/) in Google Cloud Platform.
```
SELECT
    IF
     (tips/fare >= 0.2,      
      1,
      0) AS tips,
    CAST(pickup_community_area AS string) AS pickup_community_area,
    CAST(dropoff_community_area AS string) AS dropoff_community_area,
    CAST(pickup_census_tract AS string) AS pickup_census_tract,
    CAST(dropoff_census_tract AS string) AS dropoff_census_tract,
    fare,
    EXTRACT(MONTH
      FROM
        trip_start_timestamp) AS trip_start_month,
    EXTRACT(HOUR
      FROM
        trip_start_timestamp) AS trip_start_hour,
    EXTRACT(DAYOFWEEK
      FROM
        trip_start_timestamp) AS trip_start_day,
    UNIX_SECONDS(trip_start_timestamp) AS trip_start_timestamp,
    pickup_latitude,
    pickup_longitude,
    dropoff_latitude,
    dropoff_longitude,
    trip_miles,
    payment_type,
    company,
    trip_seconds
FROM
    `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE   
    tips IS NOT NULL
    AND fare > 0
    AND (trip_miles > 0
      AND trip_miles <= 50)
    AND (trip_seconds > 0
      AND trip_seconds <= 3600)
    AND (pickup_community_area !=0
      AND pickup_community_area IS NOT NULL)
    AND (dropoff_community_area !=0
      AND dropoff_community_area IS NOT NULL)
    AND (pickup_latitude !=0
      AND pickup_latitude IS NOT NULL)
    AND (pickup_longitude !=0
      AND pickup_longitude IS NOT NULL)
    AND (dropoff_latitude !=0
      AND dropoff_latitude IS NOT NULL)
    AND (dropoff_longitude !=0
      AND dropoff_longitude IS NOT NULL)
LIMIT 1000000;
```