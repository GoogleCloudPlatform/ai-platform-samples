# Copyright 2020 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
export PROJECT_ID=YOUR PROJECT_ID
export MODEL_NAME=sentiment_classifier
export INPUT_TOPIC=projects/YOUR PROJECT_ID/topics/twitter
export REGION=us-central1
export STAGING_LOCATION=gs://YOUR BUCKET NAME/twitter/staging
export TEMP_LOCATION=gs://YOUR BUCKET NAME/twitter/tmp
export BIGQUERY_DATASET=dataset_twitter_test
export BIGQUERY_TABLE=twitter_posts_test
export GOOGLE_APPLICATION_CREDENTIALS=credentials.json
export RUNNER=DataflowRunner
export WINDOW_SIZE=60
export MIN_BATCH_SIZE=5
export MAX_BATCH_SIZE=100
