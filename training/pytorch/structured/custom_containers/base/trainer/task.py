# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the \"License\");
# you may not use this file except in compliance with the License.\n",
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an \"AS IS\" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

import experiment


def get_args():
    """Define the task arguments with the default values.

    Returns:
        experiment parameters
    """
    args_parser = argparse.ArgumentParser()

    # Data files arguments
    args_parser.add_argument(
        '--train-files',
        help='GCS or local paths to training data',
        nargs='+',
        required=True)
    args_parser.add_argument(
        '--eval-files',
        help='GCS or local paths to evaluation data',
        nargs='+',
        required=True)

    # Experiment arguments
    args_parser.add_argument(
        '--batch-size',
        help='Batch size for each training and evaluation step.',
        type=int,
        default=100)
    args_parser.add_argument(
        '--num-epochs',
        help="""\
        Maximum number of training data epochs on which to train.
        If both --train-size and --num-epochs are specified,
        --train-steps will be: (train-size/train-batch-size) * num-epochs.\
        """,
        default=50,
        type=int,
    )
    args_parser.add_argument(
        '--seed',
        help='Random seed (default: 42)',
        type=int,
        default=42,
    )

    # Feature columns arguments
    args_parser.add_argument(
        '--embed-categorical-columns',
        help="""
        If set to True, the categorical columns will be embedded
        and used in the model.
        """,
        action='store_true',
        default=True,
    )

    # Estimator arguments
    args_parser.add_argument(
        '--learning-rate',
        help='Learning rate value for the optimizers.',
        default=0.1,
        type=float)
    args_parser.add_argument(
        '--learning-rate-decay',
        help="""
      The factor by which the learning rate should decay by the end of the
      training.

      decayed_learning_rate =
        learning_rate * decay_rate ^ (global_step / decay_steps)

      If set to 0 (default), then no decay will occur.
      If set to 0.5, then the learning rate should reach 0.5 of its original
          value at the end of the training.
      Note that decay_steps is set to train_steps.
      """,
        default=0,
        type=float)
    args_parser.add_argument(
        '--test-split',
        help='split size for training / testing dataset',
        type=float,
        default=0.1,
    )

    # Saved model arguments
    args_parser.add_argument(
        '--job-dir',
        help='GCS location to export models')
    args_parser.add_argument(
        '--model-name',
        help='The name of your saved model',
        default='model.pth')

    return args_parser.parse_args()


def main():
    """Setup / Start the experiment
    """
    args = get_args()
    experiment.run(args)


if __name__ == '__main__':
    main()
