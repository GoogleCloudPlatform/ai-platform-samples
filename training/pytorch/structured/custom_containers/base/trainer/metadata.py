#!/usr/bin/env python
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Task type can be either 'classification', 'regression', or 'custom'.
# This is based on the target feature in the dataset.
TASK_TYPE = 'classification'

# List of all the columns (header) present in the input data file(s).
# Used for parsing the input data.
COLUMN_NAMES = [
    'tip',
    'trip_miles',
    'trip_seconds',
    'fare',
    'trip_start_month',
    'trip_start_hour',
    'trip_start_day',
    'pickup_community_area',
    'dropoff_community_area',
    'pickup_census_tract',
    'dropoff_census_tract',
    'pickup_latitude',
    'pickup_longitude',
    'dropoff_latitude',
    'dropoff_longitude',
    'payment_type',
    'company'
]

# List of the columns expected during serving (which is probably different to
# the header of the training data).
SERVING_COLUMN_NAMES = [
    'trip_miles',
    'trip_seconds',
    'fare',
    'trip_start_month',
    'trip_start_hour',
    'trip_start_day',
    'pickup_community_area',
    'dropoff_community_area',
    'pickup_census_tract',
    'dropoff_census_tract',
    'pickup_latitude',
    'pickup_longitude',
    'dropoff_latitude',
    'dropoff_longitude',
    'payment_type',
    'company'
]

# List of the default values of all the columns present in the input data.
# This helps decoding the data types of the columns.
DEFAULTS = [[0], [0.0], [0], [0], [0], [0], [0], [''], [''], [''], [''], [0.0],
            [0.0], [0.0], [0.0], [''], ['']]

# Dictionary of the feature names of type int or float. In the dictionary,
# the key is the feature name, and the value is another dictionary includes
# the mean and the variance of the numeric features.
# E.g. {feature_1: {mean: 0, variance:1}, feature_2: {mean: 10, variance:3}}
# The value can be set to None if you don't want to not normalize.
NUMERIC_FEATURE_NAMES_WITH_STATS = {
    'fare': None,
    'trip_miles': None,
    'trip_seconds': None
}

# Numeric features defining time of the trip.
NUMERIC_FEATURE_NAMES = {
    'trip_start_month': None,
    'trip_start_hour': None,
    'trip_start_day': None,
}

NUMERIC_FEATURE_NAMES_GEOPOINTS = {
    'pickup_latitude': None,
    'pickup_longitude': None,
    'dropoff_latitude': None,
    'dropoff_longitude': None,
}

# List of categorical columns present in the input data.
CATEGORICAL_COLUMNS = [
    'payment_type',
    'company'
]

# Dictionary of feature names with int values, but to be treated as
# categorical features. In the dictionary, the key is the feature name,
# and the value is the num_buckets (count of distinct values).
CATEGORICAL_FEATURE_NAMES_WITH_IDENTITY = {}

# Dictionary of categorical features with few nominal values. In the
# dictionary, the key is the feature name, and the value is the list of
# feature vocabulary.
CATEGORICAL_FEATURE_NAMES_WITH_VOCABULARY = {
    'payment_type': [
        'Cash', 'Credit Card', 'Pcard', 'Unknown', 'No Charge', 'Prcard',
        'Dispute', 'Mobile'
    ],
}

# Dictionary of categorical features with many values. In the dictionary,
# the key is the feature name, and the value is the number of buckets.
CATEGORICAL_FEATURE_NAMES_WITH_HASH_BUCKET = {
    'company': 100,
}

# Target feature name (response or class variable).
TARGET_NAME = 'tip'

# List of the class values (labels) in a classification dataset.
TARGET_LABELS = [1, 0]
