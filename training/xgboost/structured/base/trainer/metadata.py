# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
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

# Target name
TARGET_NAME = 'tip'

# The features to be used for training
FEATURE_NAMES = [
    'trip_miles',
    'trip_seconds',
    'fare',
    'trip_start_month',
    'trip_start_hour',
    'trip_start_day',
]

# If it is a xgboost model, saved by xgboost.Booster
# then use 'model.bst' for the model name
MODEL_FILE_NAME = 'model.bst'

# Set to True if you want to tune some hyperparameters
HYPERPARAMETER_TUNING = True

# Used only if the dataset is to be read from BigQuery
BASE_QUERY = '''
    SELECT
      *
    FROM
      `{table}`
  '''
