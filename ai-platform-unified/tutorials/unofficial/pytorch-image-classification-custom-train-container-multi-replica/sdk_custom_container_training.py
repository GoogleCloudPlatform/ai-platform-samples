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

def create_custom_container_training_job(
    project,
    staging_bucket,
    location,
    display_name,
    container_image_uri,
    container_args,
    replica_count,
    machine_type,
    accelerator_type,
    accelerator_count,
):
  aiplatform.init(project=project, staging_bucket=staging_bucket, location=location)
  custom_container_training_job = aiplatform.CustomContainerTrainingJob(
      display_name=display_name,
      container_uri=container_image_uri,
  )

  gcs_output_uri_prefix = f'gs://{staging_bucket}/{display_name}'

  custom_container_training_job.run(
      args=container_args,
      base_output_dir=gcs_output_uri_prefix,
      replica_count=replica_count,
      machine_type=machine_type,
      accelerator_type=accelerator_type,
      accelerator_count=accelerator_count,
  )

  return custom_container_training_job, gcs_output_uri_prefix

def parse_args():

  parser = argparse.ArgumentParser(
      description='PyTorch Image Classification using Multi Replica with Custom Container')
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
      '--container-image-uri', default=os.getenv('CONTAINER_IMAGE_URI'), type=str,
      help='Google Container Registry URI of the training container image')
  parser.add_argument(
      '--replica-count', default=1, type=int,
      help='The number of replica, i.e. number of compute node(s)/instance(s)')
  parser.add_argument(
      '--machine-type', default='n1-standard-4', type=str,
      help='The type of the machine supported for creating a custom training job.')
  parser.add_argument(
      '--accelerator-count', default=1, type=int,
      help='The number of accelerators to attach to the machine, i.e. number of gpu(s)')
  parser.add_argument(
      '--accelerator-type', default='NVIDIA_TESLA_P4', type=str,
      help='The type of accelerator(s) attached to the machine')
  parser.add_argument(
      '--container-args', default=None, type=str,
      help='The args when lunching container')

  args = parser.parse_args()

  return args

if __name__ == '__main__':

  args = parse_args()

  container_args = [] if not args.container_args else args.container_args.split(' ')
  custom_container_training_job, training_job_gcs_output_uri_prefix = create_custom_container_training_job(
      project=args.project,
      staging_bucket=args.bucket,
      location=args.location,
      display_name=args.display_name,
      container_image_uri=args.container_image_uri,
      container_args=container_args,
      replica_count=args.replica_count,
      machine_type=args.machine_type,
      accelerator_count=args.accelerator_count,
      accelerator_type=args.accelerator_type,
  )

  logging.info(f'Custom Container Training Job Name: {custom_container_training_job.resource_name}')
  logging.info(f'Training GCS Output URI Prefix: {training_job_gcs_output_uri_prefix}')
