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
import googleapiclient.discovery

# In this sample, we will reply on 6 features only:
# trip_miles            trip_seconds        fare
# trip_start_month      trip_start_hour     trip_start_day
instances = [
    [1.1, 420, 625, 8, 16, 3],
    [0.3, 960, 1485, 3, 22, 2],
    [1.0, 300, 505, 1, 1, 1],
]

PROJECT_ID = os.getenv('PROJECT_ID')
MODEL_NAME = os.getenv('MODEL_NAME')
MODEL_VERSION = os.getenv('MODEL_VERSION')

print('PROJECT_ID: {}'.format(PROJECT_ID))
print('MODEL_NAME: {}'.format(MODEL_NAME))
print('MODEL_VERSION: {}'.format(MODEL_VERSION))

service = googleapiclient.discovery.build('ml', 'v1')
name = 'projects/{}/models/{}/versions/{}'.format(PROJECT_ID, MODEL_NAME,
                                                  MODEL_VERSION)

response = service.projects().predict(
    name=name,
    body={'instances': instances}
).execute()

if 'error' in response:
    raise RuntimeError(response['error'])
else:
    print(response['predictions'])
