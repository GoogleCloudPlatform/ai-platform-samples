# Copyright 2021 Google LLC
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

from google.cloud import storage

def extract_bucket_and_prefix_from_gcs_path(gcs_path):

  if gcs_path.startswith("gs://"):
    gcs_path = gcs_path[5:]
  if gcs_path.endswith("/"):
    gcs_path = gcs_path[:-1]

  gcs_parts = gcs_path.split("/", 1)
  gcs_bucket = gcs_parts[0]
  gcs_blob_prefix = None if len(gcs_parts) == 1 else gcs_parts[1]

  return (gcs_bucket, gcs_blob_prefix)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
  """Uploads a file to the bucket."""

  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)

  blob.upload_from_filename(source_file_name)

  print(
      "File {} uploaded to {}.".format(
          source_file_name, destination_blob_name
      )
  )
