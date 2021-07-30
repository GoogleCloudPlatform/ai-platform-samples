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
FROM python:3.9

# Install dependencies.
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt -U

ADD PubSubToBigQueryWithAIPlatform.py /

ENV MODEL_NAME=""
ENV INPUT_TOPIC=""
ENV REGION=us-central1
ENV STAGING_LOCATION=""
ENV TEMP_LOCATION=""
ENV BIGQUERY_DATASET=""
ENV BIGQUERY_TABLE=""
ENV GOOGLE_APPLICATION_CREDENTIALS="/config"
ENV RUNNER=DataflowRunner
ENV WINDOW_SIZE=60
ENV MIN_BATCH_SIZE=1
ENV MAX_BATCH_SIZE=100

CMD python ./PubSubToBigQueryWithAIPlatform.py --input-topic=${INPUT_TOPIC} \
    --region=${REGION} \
    --staging-location=${STAGING_LOCATION} \
    --temp-location=${TEMP_LOCATION} \
    --bigquery-dataset=${BIGQUERY_DATASET} \
    --bigquery-table=${BIGQUERY_TABLE} \
    --window-size=${WINDOW_SIZE} \
    --min-batch-size=${MIN_BATCH_SIZE} \
    --max-batch-size=${MAX_BATCH_SIZE} \
    --requirements_file requirements.txt
