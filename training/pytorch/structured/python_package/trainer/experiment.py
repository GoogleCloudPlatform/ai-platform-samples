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

import hypertune
import torch

from trainer import inputs
from trainer import model


def train(sequential_model, train_loader, criterion, optimizer, epoch):
    """Create the training loop for one epoch. Read the data from the
     dataloader, calculate the loss, and update the DNN. Lastly, display some
     statistics about the performance of the DNN during training.

    Args:
      sequential_model: The neural network that you are training, based on
      nn.Module
      train_loader: The training dataset
      criterion: The loss function used during training
      optimizer: The selected optmizer to update parameters and gradients
      epoch: The current epoch that the training loop is on
    """
    sequential_model.train()
    running_loss = 0.0
    for batch_index, data in enumerate(train_loader):
        features = data['features']
        target = data['target']

        # zero the parameter gradients
        optimizer.zero_grad()
        # forward + backward + optimize
        outputs = sequential_model(features)
        loss = criterion(outputs, target)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if batch_index % 10 == 9:  # print every 10 mini-batches
            print('[epoch: %d, batch: %5d] loss: %.3f' %
                  (epoch, batch_index + 1, running_loss / 10))
            running_loss = 0.0


def test(sequential_model, test_loader, criterion, epoch, report_metric=False):
    """Test / Evaluate the DNNs performance with a test / eval dataset.
     Read the data from the dataloader and calculate the loss. Lastly,
     display some statistics about the performance of the DNN during testing.

    Args:
      sequential_model: The neural network that you are testing, based on
      nn.Module
      test_loader: The test / evaluation dataset
      criterion: The loss function
      epoch: The current epoch that the training loop is on
      report_metric: Whether to report metrics for hyperparameter tuning
    """
    sequential_model.eval()
    test_loss = 0.0
    correct = 0

    with torch.no_grad():
        for _, data in enumerate(test_loader, 0):
            features = data['features']
            target = data['target']
            output = sequential_model(features)
            # sum up batch loss
            test_loss += criterion(output, target)
            # compute accuracy for a binary classifier
            #    Values > 0.5 = 1
            #    Values <= 0.5 = 0
            correct += ((output > 0.5) == (target > 0.5)).sum().item()

    # get the average loss for the test set.
    test_loss /= (len(test_loader.sampler) / test_loader.batch_size)

    if report_metric:
      # Uses hypertune to report metrics for hyperparameter tuning.
      hpt = hypertune.HyperTune()
      hpt.report_hyperparameter_tuning_metric(
          hyperparameter_metric_tag='test_loss',
          metric_value=test_loss,
          global_step=epoch)

    # print statistics
    print('\nTest set:\n\tAverage loss: {:.4f}'.format(test_loss))
    print('\tAccuracy: {}/{} ({:.0f}%)\n'.format(
            correct,
            len(test_loader.sampler),
            100. * correct / len(test_loader.sampler)))


def run(args):
    """Load the data, train, evaluate, and export the model for serving and
     evaluating.

    Args:
      args: experiment parameters.
    """
    cuda_availability = torch.cuda.is_available()
    if cuda_availability:
      device = torch.device('cuda:{}'.format(torch.cuda.current_device()))
    else:
      device = 'cpu'
    print('\n*************************')
    print('`cuda` available: {}'.format(cuda_availability))
    print('Current Device: {}'.format(device))
    print('*************************\n')

    torch.manual_seed(args.seed)

    # Open our dataset
    train_loader, test_loader, eval_loader = inputs.load_data(args, device)

    # Create the model, loss function, and optimizer
    sequential_model, criterion, optimizer = model.create(args, device)

    # Train / Test the model
    for epoch in range(1, args.num_epochs + 1):
        train(sequential_model, train_loader, criterion, optimizer, epoch)
        test(sequential_model, test_loader, criterion,
             epoch, report_metric=True)

    # Evaluate the model
    print("Evaluate the model using the evaluation dataset")
    test(sequential_model, eval_loader, criterion,
         args.num_epochs, report_metric=False)

    # Export the trained model
    torch.save(sequential_model.state_dict(), args.model_name)

    # Save the model to GCS
    if args.job_dir:
        inputs.save_model(args)
