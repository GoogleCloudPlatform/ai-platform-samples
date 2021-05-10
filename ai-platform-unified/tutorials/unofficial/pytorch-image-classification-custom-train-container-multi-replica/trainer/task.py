"""Main program for PyTorch distributed training.

Adapted from: https://github.com/narumiruna/pytorch-distributed-example

"""

from __future__ import division, print_function

import os
import shutil
import argparse

import torch
import torch.nn.functional as F
from torch import distributed, nn
from torch.utils import data
from torchvision import datasets, transforms

import utils

def distributed_is_initialized():
  if distributed.is_available():
    if distributed.is_initialized():
      return True
  return False

class Average(object):

  def __init__(self):
    self.sum = 0
    self.count = 0

  def __str__(self):
    return '{:.6f}'.format(self.average)

  @property
  def average(self):
    return self.sum / self.count

  def update(self, value, number):
    self.sum += value * number
    self.count += number

class Accuracy(object):

  def __init__(self):
    self.correct = 0
    self.count = 0

  def __str__(self):
    return '{:.2f}%'.format(self.accuracy * 100)

  @property
  def accuracy(self):
    return self.correct / self.count

  @torch.no_grad()
  def update(self, output, target):
    pred = output.argmax(dim=1)
    correct = pred.eq(target).sum().item()

    self.correct += correct
    self.count += output.size(0)


class Trainer(object):

  def __init__(self, model, optimizer, train_loader, test_loader, device, model_name):
    self.model = model
    self.optimizer = optimizer
    self.train_loader = train_loader
    self.test_loader = test_loader
    self.device = device
    self.model_name = model_name

  def save(self, model_dir):
    model_path = os.path.join(model_dir, self.model_name)
    torch.save(self.model.state_dict(), model_path)
    print(f'model is saved to {model_path}')
    return model_path


  def fit(self, epochs):
    for epoch in range(1, epochs + 1):
      train_loss, train_acc = self.train()
      test_loss, test_acc = self.evaluate()

      print(
          'Epoch: {}/{},'.format(epoch, epochs),
          'train loss: {}, train acc: {},'.format(train_loss, train_acc),
          'test loss: {}, test acc: {}.'.format(test_loss, test_acc),
      )

  def train(self):
    self.model.train()

    train_loss = Average()
    train_acc = Accuracy()

    for data, target in self.train_loader:
      data = data.to(self.device)
      target = target.to(self.device)

      output = self.model(data)
      loss = F.cross_entropy(output, target)

      self.optimizer.zero_grad()
      loss.backward()
      self.optimizer.step()

      train_loss.update(loss.item(), data.size(0))
      train_acc.update(output, target)

    return train_loss, train_acc

  @torch.no_grad()
  def evaluate(self):
    self.model.eval()

    test_loss = Average()
    test_acc = Accuracy()

    for data, target in self.test_loader:
      data = data.to(self.device)
      target = target.to(self.device)

      output = self.model(data)
      loss = F.cross_entropy(output, target)

      test_loss.update(loss.item(), data.size(0))
      test_acc.update(output, target)

    return test_loss, test_acc


class Net(nn.Module):

  def __init__(self):
    super(Net, self).__init__()
    self.fc = nn.Linear(784, 10)

  def forward(self, x):
    return self.fc(x.view(x.size(0), -1))


class MNISTDataLoader(data.DataLoader):

  def __init__(self, root, batch_size, train=True):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),
    ])

    dataset = datasets.MNIST(root, train=train, transform=transform, download=True)
    sampler = None
    if train and distributed_is_initialized():
      sampler = data.DistributedSampler(dataset)

    super(MNISTDataLoader, self).__init__(
        dataset,
        batch_size=batch_size,
        shuffle=(sampler is None),
        sampler=sampler,
    )


def run(args):
  device = torch.device('cuda' if torch.cuda.is_available() and not args.no_cuda else 'cpu')

  model = Net()
  if distributed_is_initialized():
    model.to(device)
    model = nn.parallel.DistributedDataParallel(model)
  else:
    model = nn.DataParallel(model)
    model.to(device)

  optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)

  train_loader = MNISTDataLoader(args.root, args.batch_size, train=True)
  test_loader = MNISTDataLoader(args.root, args.batch_size, train=False)

  trainer = Trainer(
      model=model,
      optimizer=optimizer,
      train_loader=train_loader,
      test_loader=test_loader,
      device=device,
      model_name='mnist.pt'
  )
  trainer.fit(args.epochs)

  local_model_dir = './model/'
  if os.path.exists(local_model_dir) and os.path.isdir(local_model_dir):
    shutil.rmtree(local_model_dir)
  os.makedirs(local_model_dir)
  local_model_path = trainer.save(local_model_dir)

  if args.model_dir:
    gcs_bucket, gcs_blob_prefix = utils.extract_bucket_and_prefix_from_gcs_path(args.model_dir)
    utils.upload_blob(
        bucket_name=gcs_bucket,
        source_file_name=local_model_path,
        destination_blob_name=os.path.join(gcs_blob_prefix, f'{trainer.model_name}')
    )
    print(f'model is uploaded to {args.model_dir}')

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--backend',
      type=str,
      default='gloo',
      help='Name of the backend to use.')
  parser.add_argument(
      '-i',
      '--init-method',
      type=str,
      default='env://',
      help='URL specifying how to initialize the package.')
  parser.add_argument(
      '-s',
      '--world-size',
      type=int,
      default=os.environ.get('WORLD_SIZE', 1),
      help='Number of processes participating in the job.')
  parser.add_argument(
      '-r',
      '--rank',
      type=int,
      default=os.environ.get('RANK', 0),
      help='Rank of the current process.')
  parser.add_argument('--epochs', type=int, default=20)
  parser.add_argument('--no-cuda', action='store_true')
  parser.add_argument('-lr', '--learning-rate', type=float, default=1e-3)
  parser.add_argument('--root', type=str, default='data')
  parser.add_argument('--batch-size', type=int, default=128)
  parser.add_argument(
      '--model-dir', default=os.getenv('AIP_MODEL_DIR'), type=str,
      help='a Cloud Storage URI of a directory intended for saving model artifacts')
  args = parser.parse_args()
  print(args)

  if args.world_size > 1:
    distributed.init_process_group(
        backend=args.backend,
        init_method=args.init_method,
        world_size=args.world_size,
        rank=args.rank,
    )

  run(args)

if __name__ == '__main__':
  main()