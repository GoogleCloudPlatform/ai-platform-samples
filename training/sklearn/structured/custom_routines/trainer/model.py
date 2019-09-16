# Copyright 2019 Google LLC. All Rights Reserved
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

"""ML model definitions."""

from sklearn import ensemble
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline, FeatureUnion, make_pipeline
from trainer import my_pipeline as mp


def get_estimator(arguments):
    """Generate ML Pipeline which include both pre-processing and model training

    Args:
      arguments: (argparse.ArgumentParser), parameters passed from command-line

    Returns:
      structured.pipeline.Pipeline
    """

    # We want to use 5 numerical features and 1 categorical in this sample.
    numerical_indices = [0, 1, 2, 3, 4, 5]  # trip_miles, ..., trip_start_day
    categorical_indices = [14]  # 14th feature is payment_type

    p1 = make_pipeline(mp.PositionalSelector(categorical_indices),
                       mp.StripString(),
                       mp.SimpleOneHotEncoder())
    p2 = make_pipeline(mp.PositionalSelector(numerical_indices),
                       StandardScaler())

    feats = FeatureUnion([
        ('numericals', p1),
        ('categoricals', p2),
    ])

    # n_estimators and max_depth are expected to be passed as
    # command line argument to task.py
    pipeline = Pipeline([
        ('pre', feats),
        ('estimator', ensemble.RandomForestClassifier(
            n_estimators=arguments.n_estimators,
            max_depth=arguments.max_depth)
         )
    ])
    return pipeline
