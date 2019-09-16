#!/bin/bash
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

set -v

# Delete the directories created by setup.py:
rm -rf dist
rm -rf trainer.egg-info
rm -rf build
rm -rf trained

# This has to be run after train-cloud.sh is successfully executed

# Delete Cloud Storage objects that were created
gsutil -m rm -r ${MODEL_DIR}

set -
