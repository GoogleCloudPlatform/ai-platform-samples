#!/usr/bin/env python
# Copyright 2019 Google LLC. All Rights Reserved.
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

# In this sample, we will pass all available features in order.
instances = [
    [0.2, 660, 1175, 8, 10, 7, 8, 33, 17031081402, 17031330100, 41.892,
     -87.613, 41.859, -87.617, 'Credit Card', 'Taxi Affiliation Services'],
    [1.0, 300, 545, 9, 22,4 ,32, 8, 17031320100, 17031081500, 41.885,
     -87.621, 41.893, -87.626, 'Cash', 'Northwest Management LLC'],
    [1.1, 300, 565, 3, 2, 1, 28, 32, 17031833000, 17031839100, 41.885,
     -87.657, 41.881, -87.633, 'Credit Card', 'Taxi Affiliation Services']
]

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
