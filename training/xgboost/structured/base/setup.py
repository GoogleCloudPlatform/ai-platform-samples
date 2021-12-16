#!/usr/bin/env python
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

from setuptools import find_packages
from setuptools import setup

# While this is an xgboost sample, we will still require tensorflow and
# scikit-learn to be installed, since the sample uses certain functionalities
# available in those libraries:
#    tensorflow: mainly to copy files seamlessly to GCS
#    scikit-learn: the helpfer functions it provides, e.g. splitting datasets

REQUIRED_PACKAGES = [
    'tensorflow==1.15.5',
    'scikit-learn==1.0.1',
    'pandas==1.3.4',
    'xgboost==1.5.1',
    'cloudml-hypertune',
]

setup(
    name='trainer',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='AI Platform | Training | xgboost | Base'
)
