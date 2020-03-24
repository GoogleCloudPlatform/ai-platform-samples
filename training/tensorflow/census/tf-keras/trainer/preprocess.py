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

import pandas as pd

import util

_CSV_COLUMNS = [
    'age', 'workclass', 'fnlwgt', 'education', 'education_num',
    'marital_status', 'occupation', 'relationship', 'race', 'gender',
    'capital_gain', 'capital_loss', 'hours_per_week', 'native_country',
    'income_bracket'
]

# This is the label (target) we want to predict.
_LABEL_COLUMN = 'income_bracket'


class Preprocessor(object):
    def __init__(self):
        self.train_x, self.train_y, self.eval_x, self.eval_y = \
            self._initialize(util.DATA_DIR)

    def preprocess(self, instances):
        """Preprocess instances for prediction, by removing some columns, and
        converting categorical columns to numeric values.
        Example:

        {"instances": [[25,'Private',226802,'11th',7,'Never-married',
        'Machine-op-inspct','Own-child','Black','Male',0,0,40,'United-States']]}

        :param instances: An array.
        :return:
        """
        # Join train_x and eval_x to normalize on overall means and standard
        # deviations. Then separate them again.
        dataframe = pd.DataFrame(instances, columns=_CSV_COLUMNS[:-1])
        predictions = util.preprocess(dataframe)
        all_x = pd.concat([self.train_x, self.eval_x, predictions],
                          keys=['train', 'eval', 'predict'], sort=False)
        all_x = util.standardize(all_x)
        predictions = all_x.xs('predict')
        return predictions

    def _initialize(self, data_dir):
        """

        :param data_dir:
        :return:
        """
        training_file_path, eval_file_path = util.download(data_dir)

        # This census data uses the value '?' for missing entries. We use
        # na_values to find ? and set it to NaN.
        # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv
        # .html
        train_df = pd.read_csv(training_file_path, names=_CSV_COLUMNS,
                               na_values='?')
        eval_df = pd.read_csv(eval_file_path, names=_CSV_COLUMNS, na_values='?')

        train_df = util.preprocess(train_df)
        eval_df = util.preprocess(eval_df)

        # Split train and eval data with labels. The pop method copies and
        # removes
        # the label column from the dataframe.
        train_x, train_y = train_df, train_df.pop(_LABEL_COLUMN)
        eval_x, eval_y = eval_df, eval_df.pop(_LABEL_COLUMN)
        return train_x, train_y, eval_x, eval_y
