#!/usr/bin/env python
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import tensorflow as tf

from . import featurizer
from . import metadata


def create(args, config):
    """ Create a DNNLinearCombinedEstimator based on metadata.TASK_TYPE

    Args:
      args: experiment parameters.
      config: tf.RunConfig object. Returns DNNLinearCombinedClassifier or
        DNNLinearCombinedRegressor
    """

    wide_columns, deep_columns = featurizer.create_wide_and_deep_columns(args)
    logging.info('Wide columns: {}'.format(wide_columns))
    logging.info('Deep columns: {}'.format(deep_columns))

    # Change the optimizers for the wide and deep parts of the model if you wish
    linear_optimizer = tf.compat.v1.train.FtrlOptimizer(learning_rate=args.learning_rate)
    # Use _update_optimizer to implement an adaptive learning rate

    def predicate(): return _update_optimizer(args)

    dnn_optimizer = predicate

    if metadata.TASK_TYPE == 'classification':
        estimator = tf.estimator.DNNLinearCombinedClassifier(
            n_classes=len(metadata.TARGET_LABELS),
            linear_optimizer=linear_optimizer,
            linear_feature_columns=wide_columns,
            dnn_feature_columns=deep_columns,
            dnn_optimizer=dnn_optimizer,
            dnn_hidden_units=_construct_hidden_units(args),
            dnn_activation_fn=tf.nn.relu,
            dnn_dropout=args.dropout_prob,
            batch_norm=True,
            config=config,
        )
    else:
        estimator = tf.estimator.DNNLinearCombinedRegressor(
            linear_optimizer=linear_optimizer,
            linear_feature_columns=wide_columns,
            dnn_feature_columns=deep_columns,
            dnn_optimizer=dnn_optimizer,
            dnn_hidden_units=_construct_hidden_units(args),
            dnn_activation_fn=tf.nn.relu,
            dnn_dropout=args.dropout_prob,
            batch_norm=True,
            config=config,
        )

    return estimator


def _construct_hidden_units(args):
    """ Create the number of hidden units in each layer

    If the args.layer_sizes_scale_factor > 0 then it will use a "decay"
    mechanism
    to define the number of units in each layer. Otherwise, arg.hidden_units
    will be used as-is.

    Args:
      args: experiment parameters.
    Returns:
        list of int
    """
    hidden_units = [int(units) for units in args.hidden_units.split(',')]

    if args.layer_sizes_scale_factor > 0:
        first_layer_size = hidden_units[0]
        scale_factor = args.layer_sizes_scale_factor
        num_layers = args.num_layers

        hidden_units = [
            max(2, int(first_layer_size * scale_factor ** i))
            for i in range(num_layers)
        ]

    logging.info('Hidden units structure: {}'.format(hidden_units))
    return hidden_units


def _update_optimizer(args):
    """Create an optimizer with an update learning rate.

    Args:
      args: experiment parameters
    Returns:
      Optimizer
    """
    # Decayed_learning_rate = learning_rate * decay_rate ^ (global_step /
    # decay_steps)
    # See: https://www.tensorflow.org/api_docs/python/tf/train/exponential_decay
    learning_rate = tf.train.exponential_decay(
        learning_rate=args.learning_rate,
        global_step=tf.train.get_or_create_global_step(),
        decay_steps=args.train_steps,
        decay_rate=args.learning_rate_decay_factor)

    tf.summary.scalar('learning_rate', learning_rate)

    # By default, AdamOptimizer is used. You can change the type of the
    # optimizer.
    return tf.train.AdamOptimizer(learning_rate=learning_rate)
