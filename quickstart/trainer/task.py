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

"""Executes model training"""

import sys
import os.path
import logging
import tensorflow as tf

from sklearn.externals import joblib
from sklearn.linear_model import LinearRegression


def get_dummy_data(n):
    r = range(n)
    X = [[x] for x in r]
    Y = [2 * x + 1 for x in r]
    return X, Y


def main():
    logging.basicConfig()
    model = LinearRegression()
    X, Y = get_dummy_data(100)
    model.fit(X, Y)

    # The model name should remain 'model.joblib' for
    # AI Platform to be able to create a model version.
    model_name = os.path.join(sys.argv[1], 'model.joblib')
    logging.info('Model will be saved to "%s..."', model_name)
    temp_file = '/tmp/model.joblib'
    joblib.dump(model, temp_file)

    # Copy the temporary model file to its destination
    with tf.io.gfile.GFile(temp_file, 'rb') as temp_file_object:
        with tf.io.gfile.GFile(model_name, 'wb') as file_object:
            file_object.write(temp_file_object.read())

    logging.info('Model was saved')


if __name__ == '__main__':
    main()
