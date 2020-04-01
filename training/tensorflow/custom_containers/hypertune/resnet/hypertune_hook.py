# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
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
"""Communicate evaluation results to hyperparmeter tuning servicer."""
import os

import hypertune
import tensorflow as tf


class HypertuneHook(tf.train.SessionRunHook):
    """."""

    def __init__(self, metric_tensor_name):
        self.hypertune = hypertune.HyperTune()
        self.hp_metric_tag = os.environ.get('CLOUD_ML_HP_METRIC_TAG', '')
        self.trial_id = os.environ.get('CLOUD_ML_TRIAL_ID', 0)
        self.tensor_name = metric_tensor_name

    def end(self, session):
        step_variable = session.graph.get_collection('global_step')
        global_step = session.run(step_variable)[0]

        tf.logging.info('HypertuneHook called, tag: {}, trial_id: {}, global_step: {}'.format(self.hp_metric_tag, self.trial_id, global_step))

        metric_tensor = session.graph.get_tensor_by_name(
            self.tensor_name+'/value:0')

        metric_value = session.run(metric_tensor)

        self.hypertune.report_hyperparameter_tuning_metric(
            hyperparameter_metric_tag=self.hp_metric_tag,
            metric_value=metric_value,
            global_step=global_step)

