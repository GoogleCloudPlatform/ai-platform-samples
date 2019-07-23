# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the \"License\");
# you may not use this file except in compliance with the License.\n",
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an \"AS IS\" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Install pytorch
FROM gcr.io/deeplearning-platform-release/pytorch-gpu.1-1
# OR
# FROM pytorch/pytorch:1.0.1-cuda10.0-cudnn7-runtime

WORKDIR /root

# Installs pandas, and google-cloud-storage.
RUN pip install pandas google-cloud-storage

# The data for this sample has been publicly hosted on a GCS bucket.
# You can modify this by changing the arguments passed into the Dockerfile
ARG TRAIN_FILES=https://storage.googleapis.com/cloud-samples-data/ml-engine/chicago_taxi/training/small/taxi_trips_train.csv
ARG EVAL_FILES=https://storage.googleapis.com/cloud-samples-data/ml-engine/chicago_taxi/training/small/taxi_trips_eval.csv

# Download the data from the public Google Cloud Storage bucket for this sample
RUN curl $TRAIN_FILES --output ./taxi_trips_train.csv
RUN curl $EVAL_FILES --output ./taxi_trips_eval.csv

# Copies the trainer code to the docker image.
COPY trainer/experiment.py ./trainer/experiment.py
COPY trainer/inputs.py ./trainer/inputs.py
COPY trainer/metadata.py ./trainer/metadata.py
COPY trainer/model.py ./trainer/model.py
COPY trainer/task.py ./trainer/task.py

# Set up the entry point to invoke the trainer.
ENTRYPOINT ["python", "-u", "trainer/task.py"]