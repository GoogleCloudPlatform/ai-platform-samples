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

import torch.optim as optim
import torch.nn as nn


# Specify the Deep Neural model
class SequentialDNN(nn.Module):
    def __init__(self):
        """Defines a simple DNN for this template, it is recommended that you
        modify this to match your data / model needs.
        """
        super(SequentialDNN, self).__init__()

        self.sequential_model = nn.Sequential(
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 4),
            nn.ReLU(),
            nn.Linear(4, 1),
        )

    def forward(self, x):
        return self.sequential_model(x)


def create(args, device):
    """
    Create the model, loss function, and optimizer to be used for the DNN

    Args:
      args: experiment parameters.
    """
    sequential_model = SequentialDNN().double().to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(sequential_model.parameters(),
                           lr=args.learning_rate,
                           weight_decay=args.weight_decay)

    return sequential_model, criterion, optimizer
