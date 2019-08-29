#!/usr/bin/env python
# Copyright 2019 Google LLC. All Rights Reserved.
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
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import DenseFeatures, Dense, concatenate
from tensorflow.keras.layers import Dropout, BatchNormalization

from . import featurizer
from . import metadata


def create(args, config):
    """ Create a tf.keras Wide & Deep based on metadata.TASK_TYPE
    Args:
      args: experiment parameters.
      config: tf.RunConfig object. Returns a Classifier or Regressor
    """

    wide_columns, deep_columns = featurizer.create_wide_and_deep_columns(args)
    logging.info('Wide columns: {}'.format(wide_columns))
    logging.info('Deep columns: {}'.format(deep_columns))

    # Change the optimizers for the wide and deep parts of the model if you wish
    linear_optimizer = tf.train.FtrlOptimizer(learning_rate=args.learning_rate)
    # Use _update_optimizer to implement an adaptive learning rate

    def predicate(): return _update_optimizer(args)

    dnn_optimizer = predicate

    n_classes = len(metadata.TARGET_LABELS) if metadata.TASK_TYPE == 'classification' else 1

    return _create_wide_n_deep(
            n_classes=len(metadata.TARGET_LABELS),
            linear_feature_columns=wide_columns,
            linear_optimizer=linear_optimizer,            
            dnn_feature_columns=deep_columns,
            dnn_optimizer=dnn_optimizer,
            dnn_hidden_units=_construct_hidden_units(args),
            dnn_activation_fn=tf.nn.relu,
            dnn_dropout=args.dropout_prob,
            batch_norm=True,
            config=config,
        )

def _create_wide_n_deep(linear_feature_columns,
                linear_optimizer,
                dnn_feature_columns,
                dnn_optimizer,
                dnn_hidden_units,            
                config,
                dnn_dropout=0,   
                batch_norm=True,
                dnn_activation_fn=tf.nn.relu, 
                n_classes=1
               ):
    """ Create a Wide and Deep model """
    
    # The input vector
    inputs = Input((len(dnn_feature_columns) + len(linear_feature_columns),))
        
    # Create the wide model
    wide = _create_wide_model(dnn_feature_columns, dnn_hidden_units, inputs, activation, dnn_dropout, batch_norm)
    
    # Create the deep model
    deep = _create_deep_model()
    
    # Concatenate the outputs from both models
    both = concatenate([wide, deep])
    
    # Add the binary (logistic) classifier
    output = Dense(1, activation='sigmoid')(both)
    model = Model(inputs, output)
    # Note: tf.keras does not yet support specifying multiple optimizers in the compile step,
    # hence we use a single optimizer for both the wide and deep networks
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return both
    
def _create_wide_model(linear_feature_columns, inputs):
    """ Create the wide model """
    wide = DenseFeatures(linear_feature_columns)(inputs)
    return wide

def _create_deep_model(dnn_feature_columns, dnn_hidden_units, inputs, activation=tf.nn.relu, dnn_dropout=0, batch_norm=True):
    """ Create the deep model """
    
    # Start with Dense Features layer
    deep = DenseFeatures(dnn_feature_columns)(inputs)
    
    # Add the hidden Dense layers
    for layerno, numnodes in enumerate(dnn_hidden_units):
        deep = Dense(numnodes, activation=activation)(deep)  
        
        # Add batch normalization after each hidden layer
        if batch_norm is True:
            deep = BatchNormalization()(deep)
        # Add dropout after each hidden layer
        if dnn_dropout > 0:
            deep = Dropout(dropout)(deep)
    return deep
