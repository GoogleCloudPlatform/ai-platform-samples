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

"""Hold utility functions."""

import os

import ntpath
import pickle
import pandas as pd
import tensorflow as tf

from sklearn import model_selection as ms
from sklearn.externals import joblib

from trainer import metadata


def data_train_test_split(data_df):
    """Split the DataFrame two subsets for training and testing.

    Args:
      data_df: (pandas.DataFrame) DataFrame the splitting to be performed on

    Returns:
      A Tuple of (pandas.DataFrame, pandas.Series,
                  pandas.DataFrame, pandas.Series)
    """

    # Only use metadata.FEATURE_NAMES + metadata.TARGET_NAME
    features = data_df[metadata.FEATURE_NAMES]
    target = data_df[metadata.TARGET_NAME]

    x_train, x_val, y_train, y_val = ms.train_test_split(features,
                                                         target,
                                                         test_size=0.2)
    return x_train.values, y_train, x_val.values, y_val


def read_df_from_bigquery(full_table_path, project_id=None, num_samples=None):
    """Read data from BigQuery and split into train and validation sets.

    Args:
      full_table_path: (string) full path of the table containing training data
        in the format of [project_id.dataset_name.table_name].
      project_id: (string, Optional) Google BigQuery Account project ID.
      num_samples: (int, Optional) Number of data samples to read.

    Returns:
      pandas.DataFrame
    """

    query = metadata.BASE_QUERY.format(table=full_table_path)
    limit = ' LIMIT {}'.format(num_samples) if num_samples else ''
    query += limit

    # Use "application default credentials"
    # Use SQL syntax dialect
    data_df = pd.read_gbq(query, project_id=project_id, dialect='standard')

    return data_df


def read_df_from_gcs(file_pattern):
    """Read data from Google Cloud Storage, split into train and validation sets.

    Assume that the data on GCS is in csv format without header.
    The column names will be provided through metadata

    Args:
      file_pattern: (string) pattern of the files containing training data.
      For example: [gs://bucket/folder_name/prefix]

    Returns:
      pandas.DataFrame
    """

    # Download the files to local /tmp/ folder
    df_list = []

    for filepath in tf.io.gfile.glob(file_pattern):
        with tf.io.gfile.GFile(filepath, 'r') as f:
            if metadata.CSV_COLUMNS is None:
                df_list.append(pd.read_csv(f))
            else:
                df_list.append(pd.read_csv(f, names=metadata.CSV_COLUMNS,
                                           header=None))

    data_df = pd.concat(df_list)

    return data_df


def copy_file(old_path, new_path):
    """Copy the file from old_path to new_path
    The paths can be local or on GCS

    Args:
      old_path: (string) original file location
      new_path: (string) new location and name for the file to be copied to

    Returns:
      None
    """

    # Make sure the local nested directory already exists:
    out_dir = ntpath.split(new_path)[0]
    if not (out_dir.startswith('gs://') and os.path.exists(out_dir)):
        os.makedirs(out_dir)

    tf.io.gfile.copy(old_path, new_path, overwrite=True)


def save_model(estimator, output_path, how='pickle'):
    temp_file = '/tmp/modelfile'
    if how == 'pickle':
        pickle.dump(estimator, open(temp_file, 'w'))
    elif how == 'pickle':
        joblib.dump(estimator, open(temp_file, 'w'))
    elif how == 'bst':
        estimator.save_model(temp_file)
    else:
        raise Exception('Unknown method for saving: %s' % how)

    copy_file(temp_file, output_path)


def dump_object(object_to_dump, output_path):
    """Pickle the object and save to the output_path.

    Args:
      object_to_dump: Python object to be pickled
      output_path: (string) output path which can be Google Cloud Storage

    Returns:
      None
    """

    if not tf.io.gfile.exists(output_path):
        tf.io.gfile.makedirs(os.path.dirname(output_path))
    with tf.io.gfile.GFile(output_path, 'w') as wf:
        joblib.dump(object_to_dump, wf)


def boolean_mask(columns, target_columns):
    """Create a boolean mask indicating location of target_columns in columns.

    Args:
      columns: (List[string]), list of all columns considered.
      target_columns: (List[string]), columns whose position
        should be masked as 1.

    Returns:
      List[bool]
    """
    target_set = set(target_columns)
    return [x in target_set for x in columns]
