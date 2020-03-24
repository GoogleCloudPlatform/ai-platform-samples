# Copyright 2020 Google LLC
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
"""This script is part of custom prediction."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle

from tensorflow import keras


class MyPredictor(object):
    def __init__(self, model, preprocessor):
        self._model = model
        self._preprocessor = preprocessor

    def predict(self, instances):
        instances = self._preprocessor.preprocess(instances)
        outputs = self._model.predict(instances)
        return outputs

    @classmethod
    def from_path(cls, model_dir):
        model = keras.models.load_model(model_dir)
        preprocessor_path = os.path.join(model_dir, 'preprocessor.pkl')
        with open(preprocessor_path, 'rb') as f:
            preprocessor = pickle.load(f)

        return cls(model, preprocessor)