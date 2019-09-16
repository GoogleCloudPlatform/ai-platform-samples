#!/usr/bin/env python
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

import os
import logging
import googleapiclient.discovery

logging.basicConfig()

instances = [[1000], [2000]]

PROJECT_ID = os.getenv('PROJECT_ID')
MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_VERSION = os.getenv('MODEL_VERSION')

logging.info('PROJECT_ID: %s', PROJECT_ID)
logging.info('MODEL_NAME: %s', MODEL_NAME)
logging.info('MODEL_VERSION: %s', MODEL_VERSION)

service = googleapiclient.discovery.build('ml', 'v1')
name = 'projects/{}/models/{}/versions/{}'.format(PROJECT_ID, MODEL_NAME,
                                                  MODEL_VERSION)

response = service.projects().predict(
    name=name,
    body={'instances': instances}
).execute()

if 'error' in response:
    logging.error(response['error'])
else:
    print(response['predictions'])
