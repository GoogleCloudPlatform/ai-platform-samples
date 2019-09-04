# Copyright 2019 Google LLC. All Rights Reserved.
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

"""Executes model training and evaluation."""

import argparse
import logging
import os

import hypertune
import numpy as np
from datetime import datetime
from sklearn import model_selection
from trainer import metadata
from trainer import model
from trainer import utils


def _train_and_evaluate(estimator, dataset, output_dir):
    """Runs model training and evaluation.

    Args:
      estimator: (pipeline.Pipeline), Pipeline instance, assemble pre-processing
        steps and model training
      dataset: (pandas.DataFrame), DataFrame containing training data
      output_dir: (string), directory that the trained model will be exported

    Returns:
      None
    """
    x_train, y_train, x_val, y_val = utils.data_train_test_split(dataset)
    estimator.fit(x_train, y_train)

    # Write model and eval metrics to `output_dir`
    model_output_path = os.path.join(output_dir, 'model',
                                     metadata.MODEL_FILE_NAME)

    utils.dump_object(estimator, model_output_path)

    if metadata.HYPERPARAMTER_TUNING:
        # Note: for now, use `cross_val_score` defaults (i.e. 3-fold)
        scores = model_selection.cross_val_score(estimator, x_val, y_val, cv=3)

        logging.info('Scores: %s', scores)

        # The default name of the metric is training/hptuning/metric.
        # We recommend that you assign a custom name
        # The only functional difference is that if you use a custom name,
        # you must set the hyperparameterMetricTag value in the
        # HyperparameterSpec object in the job request to match your chosen name
        hpt = hypertune.HyperTune()
        hpt.report_hyperparameter_tuning_metric(
            hyperparameter_metric_tag='Taxi Model Accuracy',
            metric_value=np.mean(scores),
            global_step=900)


def run_experiment(arguments):
    """Testbed for running model training and evaluation."""
    # Get data for training and evaluation

    logging.info('Arguments: %s', arguments)

    dataset = utils.read_df_from_gcs(arguments.input)

    # Get estimator
    estimator = model.get_estimator(arguments)

    # Run training and evaluation
    _train_and_evaluate(estimator, dataset, arguments.job_dir)


def _parse_args():
    """Parses command-line arguments."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--log-level',
        help='Logging level.',
        choices=[
            'DEBUG',
            'ERROR',
            'FATAL',
            'INFO',
            'WARN',
        ],
        default='INFO',
    )

    parser.add_argument(
        '--input',
        help='''Dataset to use for training and evaluation.
              Can be BigQuery table or a file (CSV).
              If BigQuery table, specify as as PROJECT_ID.DATASET.TABLE_NAME.
            ''',
        required=True,
    )

    parser.add_argument(
        '--job-dir',
        help='Output directory for exporting model and other metadata.',
        required=True,
    )

    parser.add_argument(
        '--n-estimators',
        help='Number of trees in the forest.',
        default=10,
        type=int,
    )

    parser.add_argument(
        '--max-depth',
        help='The maximum depth of the tree.',
        type=int,
        default=3,
    )

    return parser.parse_args()


def main():
    """Entry point"""

    arguments = _parse_args()
    logging.basicConfig(level=arguments.log_level)
    # Run the train and evaluate experiment
    time_start = datetime.utcnow()
    run_experiment(arguments)
    time_end = datetime.utcnow()
    time_elapsed = time_end - time_start
    logging.info('Experiment elapsed time: {} seconds'.format(
        time_elapsed.total_seconds()))


if __name__ == '__main__':
    main()
