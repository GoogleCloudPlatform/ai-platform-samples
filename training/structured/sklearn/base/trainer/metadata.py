# Copyright 2019 Google Inc. All Rights Reserved.
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
# ==============================================================================

"""Dataset metadata."""

# If the input CSV file has a header row, then set CSV_COLUMNS to None.
# Otherwise, set CSV_COLUMNS to a list of target and feature names:
CSV_COLUMNS = None


TARGET_NAME = 'tip'


NUMERIC_FEATURES = [
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
    ]


CATEGORICAL_FEATURES = [
    'payment_type',
    'company']


FEATURE_COLUMNS = NUMERIC_FEATURES


METRIC_FILE_NAME = 'eval_metrics.joblib'
MODEL_FILE_NAME = 'model.joblib'

BASE_QUERY = '''
    SELECT
      *
    FROM
      `{table}`
  '''
