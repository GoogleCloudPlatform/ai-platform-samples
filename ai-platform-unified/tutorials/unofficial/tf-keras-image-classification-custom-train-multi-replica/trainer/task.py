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
import pathlib
import logging
import json

from google.cloud import storage

import tensorflow as tf
from tensorflow.keras import layers

logging.basicConfig(level=logging.INFO)

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

def download_data():
  dataset_url = "https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz"
  data_dir = tf.keras.utils.get_file(
      origin=dataset_url,
      fname='flower_photos',
      untar=True
  )
  data_dir = pathlib.Path(data_dir)
  return data_dir

def load_dataset(data_dir, validation_split, seed, img_height, img_width, batch_size):
  train_ds = tf.keras.preprocessing.image_dataset_from_directory(
      data_dir,
      validation_split=validation_split,
      subset="training",
      seed=seed,
      image_size=(img_height, img_width),
      batch_size=batch_size)

  val_ds = tf.keras.preprocessing.image_dataset_from_directory(
      data_dir,
      validation_split=validation_split,
      subset="validation",
      seed=seed,
      image_size=(img_height, img_width),
      batch_size=batch_size)

  return train_ds, val_ds

def build_model(num_classes):

  model = tf.keras.Sequential([
      layers.experimental.preprocessing.Rescaling(1./255),
      layers.Conv2D(32, 3, activation='relu'),
      layers.MaxPooling2D(),
      layers.Conv2D(32, 3, activation='relu'),
      layers.MaxPooling2D(),
      layers.Conv2D(32, 3, activation='relu'),
      layers.MaxPooling2D(),
      layers.Flatten(),
      layers.Dense(128, activation='relu'),
      layers.Dense(num_classes)
  ])

  model.compile(
      optimizer='adam',
      loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
      metrics=['accuracy'])

  return model

def train(model, train_ds, val_ds, epochs, tensorboard_log_dir):

  tensorboard_callback = tf.keras.callbacks.TensorBoard(
      log_dir=tensorboard_log_dir,
      update_freq=1
  )

  history = model.fit(
      train_ds,
      validation_data=val_ds,
      epochs=epochs,
      callbacks=[tensorboard_callback]
  )
  return history

def main():

  args = parse_args()

  devices_gpu = tf.config.list_physical_devices('GPU')
  logging.info(f'Num GPUs Available: {len(devices_gpu)}')

  if args.replica_count > 1:
    strategy = tf.distribute.MultiWorkerMirroredStrategy()
  elif args.replica_count == 1:
    strategy = tf.distribute.MirroredStrategy()

  logging.info(f'Replica count: {args.replica_count}')
  logging.info(f'Number of replicas in sync: {strategy.num_replicas_in_sync}')
  tf_config = os.getenv('TF_CONFIG', None)
  num_workers = 1
  if tf_config:
    tf_config = json.loads(tf_config)
    logging.info(f'TF-Config: {tf_config}')
    num_workers = len(tf_config['cluster']['worker'])
  logging.info(f'Number of workers: {num_workers}')
  global_batch_size = args.batch_size * num_workers
  logging.info(f'Global batch size: {global_batch_size}')

  local_model_dir = './model'
  tensorboard_log_dir = args.tensorboard_log_dir if args.tensorboard_log_dir else './logs'

  data_dir = download_data()
  image_count = len(list(data_dir.glob('*/*.jpg')))
  logging.info(f'Downloaded {image_count} images')

  train_ds, val_ds = load_dataset(
      data_dir,
      args.validation_split,
      args.seed,
      args.img_height,
      args.img_width,
      global_batch_size
  )

  class_names = train_ds.class_names
  num_classes = len(class_names)
  logging.info(f'Number of classes: {num_classes}')
  logging.info(f'Class namees: {class_names}')

  # Open a strategy scope.
  with strategy.scope():
    # Everything that creates variables should be under the strategy scope.
    # In general this is only model construction & `compile()`.
    model = build_model(num_classes)

  history = train(model, train_ds, val_ds, args.epochs, tensorboard_log_dir)

  logging.info(f'Tensorboard logs are saved to: {tensorboard_log_dir}')

  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']

  loss = history.history['loss']
  val_loss = history.history['val_loss']

  logging.info('Training accuracy: {acc}, loss: {loss}'.format(
      acc=acc[-1], loss=loss[-1]))
  logging.info('Validation accuracy: {acc}, loss: {loss}'.format(
      acc=val_acc[-1], loss=val_loss[-1]))

  local_model_path = os.path.join(local_model_dir, str(args.model_version))
  model.save(local_model_path)
  logging.info(f'Model version {args.model_version} is saved to {local_model_dir}')

  if args.model_dir:

    gcs_bucket, gcs_blob_prefix = extract_bucket_and_prefix_from_gcs_path(args.model_dir)
    for subdir, dirs, files in os.walk(local_model_dir):
      for file in files:
        source_file_name = os.path.join(subdir, file)
        destination_blob_name=os.path.join(gcs_blob_prefix, file)
        upload_blob(
            bucket_name=gcs_bucket,
            source_file_name=source_file_name,
            destination_blob_name=destination_blob_name)

    logging.info(f'Model version {args.model_version} is uploaded to {args.model_dir}')

  return

def parse_args():
  parser = argparse.ArgumentParser(
      description='Keras Image Classification using Multi Replica with Custom Script')
  parser.add_argument(
      '--replica-count', default=1, type=int,
      help='number of training epochs')
  parser.add_argument(
      '--epochs', default=25, type=int,
      help='number of training epochs')
  parser.add_argument(
      '--batch-size', default=32, type=int,
      help='mini-batch size')
  parser.add_argument(
      '--img-height', default=180, type=int,
      help='image height')
  parser.add_argument(
      '--img-width', default=180, type=int,
      help='image width')
  parser.add_argument(
      '--validation-split', default=0.2, type=float,
      help='validation split ratio')
  parser.add_argument(
      '--seed', default=123, type=int,
      help='seed')
  parser.add_argument(
      '--model-version', default=1, type=int,
      help='model version')

  # Using environment variables for Cloud Storage directories
  # If you specify the baseOutputDirectory API field, AI Platform sets the
  # following environment variables when it runs your training code:
  parser.add_argument(
      '--model-dir', default=os.getenv('AIP_MODEL_DIR'), type=str,
      help='a Cloud Storage URI of a directory intended for saving model artifacts')
  parser.add_argument(
      '--tensorboard-log-dir', default=os.getenv('AIP_TENSORBOARD_LOG_DIR'), type=str,
      help='a Cloud Storage URI of a directory intended for saving TensorBoard')

  args = parser.parse_args()

  return args

if __name__ == '__main__':
  main()
