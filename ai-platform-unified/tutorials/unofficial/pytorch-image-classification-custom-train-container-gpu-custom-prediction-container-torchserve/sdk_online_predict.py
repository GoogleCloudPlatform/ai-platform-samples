# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import argparse
import logging

from google.cloud import aiplatform
import base64

logging.basicConfig(level=logging.INFO)

def convert_b64(input_file_name):
  """Open image and convert it to Base64"""
  with open(input_file_name, 'rb') as input_file:
    jpeg_bytes = base64.b64encode(input_file.read()).decode('utf-8')
  return jpeg_bytes

def predict(
    project,
    location,
    endpoint_name,
    image_file_name,
):

  aiplatform.init(project=project, location=location)
  endpoint = aiplatform.Endpoint(endpoint_name=endpoint_name)
  instance = {"data": {"b64": convert_b64(image_file_name)}}
  prediction = endpoint.predict(instances=[instance])

  return prediction

def parse_args():

  parser = argparse.ArgumentParser(
      description='Serve PyTorch Image Classification Model using TorchServe with Custom Container')
  parser.add_argument(
      '--project', default=os.getenv('PROJECT'), type=str,
      help='Google Cloud project ID')
  parser.add_argument(
      '--location', default=os.getenv('LOCATION'), type=str,
      help='Google Cloud project location')
  parser.add_argument(
      '--bucket', default=os.getenv('BUCKET'), type=str,
      help='Google Cloud bucket used for staging')
  parser.add_argument(
      '--endpoint-name', type=str,
      help='The deployed Google Cloud Endpoint to serve online prediction')
  parser.add_argument(
      '--image-file-name', type=str,
      help='Local image file name for prediction')
  args = parser.parse_args()

  return args

if __name__ == '__main__':

  args = parse_args()

  result = predict(
      project=args.project,
      location=args.location,
      endpoint_name=args.endpoint_name,
      image_file_name=args.image_file_name
  )

  logging.info(f'Prediction: {result}')
