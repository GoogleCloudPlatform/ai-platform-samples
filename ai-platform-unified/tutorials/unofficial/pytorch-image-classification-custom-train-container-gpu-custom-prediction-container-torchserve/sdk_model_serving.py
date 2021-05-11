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

logging.basicConfig(level=logging.INFO)

def serve_model(
    project,
    location,
    model_display_name,
    model_serving_container_image_uri,
):

  aiplatform.init(project=project, location=location)
  model_name = "antandbee"
  model = aiplatform.Model.upload(
      display_name=model_display_name,
      serving_container_image_uri=model_serving_container_image_uri,
      serving_container_ports=[8080],
      serving_container_predict_route=f"/predictions/{model_name}",
      serving_container_health_route="/ping",
  )
  endpoint = model.deploy(
      machine_type="n1-standard-4",
  )

  return model, endpoint

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
      '--display-name', type=str, help='Training display name')
  parser.add_argument(
      '--model-serving-container-image-uri', default=os.getenv('MODEL_SERVING_CONTAINER_IMAGE_URI'), type=str,
      help='')

  args = parser.parse_args()

  return args

if __name__ == '__main__':

  args = parse_args()

  model, endpoint = serve_model(
      project=args.project,
      location=args.location,
      model_display_name=args.display_name,
      model_serving_container_image_uri=args.model_serving_container_image_uri,
  )

  logging.info(f'Model: {model.resource_name}')
  logging.info(f'Endpoint: {endpoint.resource_name}')

