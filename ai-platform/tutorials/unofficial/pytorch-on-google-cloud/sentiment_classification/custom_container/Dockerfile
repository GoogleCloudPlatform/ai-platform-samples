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
FROM gcr.io/cloud-aiplatform/training/pytorch-gpu.1-7

WORKDIR /root

# Installs pandas, and google-cloud-storage.
RUN pip install google-cloud-storage transformers datasets tqdm

# Copies the trainer code to the docker image.
COPY ./trainer/__init__.py ./trainer/__init__.py
COPY ./trainer/experiment.py ./trainer/experiment.py
COPY ./trainer/utils.py ./trainer/utils.py
COPY ./trainer/metadata.py ./trainer/metadata.py
COPY ./trainer/model.py ./trainer/model.py
COPY ./trainer/task.py ./trainer/task.py

# Set up the entry point to invoke the trainer.
ENTRYPOINT ["python", "-m", "trainer.task"]
