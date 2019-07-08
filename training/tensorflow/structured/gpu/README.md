# AI Platform Training

## Overview

You can run your training jobs on AI Platform with graphics processing units
(GPUs). GPUs are designed to perform mathematically intensive operations at
high speed. They can be more effective at running certain operations on tensor
data than adding another machine with one or more CPU cores.

The AI Platform training service doesn't provide any special interface for
working with GPUs. You can specify GPU-enabled machines to run your job, and
the service allocates them for you. When you specify a machine type with GPU
access for a task type, each instance assigned to that task type is configured
identically (as always): the service runs a single replica of your code on each
machine.

In this example we will use `MirroredStrategy` to execute model training.
`create_run_config` in `experiment.py`  already contains the code to use GPUs.
This file is in the trainer folder under:
  `training/structured/tensorflow/base/trainer`

## Prerequisites

## Prerequisites

* Setup your project by following the instructions in the [setup](../../../../setup) folder.
  Run [variables.sh](../../../../setup/variables.sh) in [setup](../../../../setup) folder.
  
 ```bash
    source ./variables.sh
 ```
 
* Download the datasets using [download-taxi.sh](../../../../datasets/download-taxi.sh) in [datasets](../../../../datasets) 
folder.

 ```bash
    source ./download-taxi.sh /your_local_datasets_dir/
 ```
* Create a Python 3 virtual environment and activate it.
* Change the directory to this sample and run: 

  ```
  python setup.py install
  ```
  
  Optional: You can also run:
  ```
  pip install -r requirements.txt
  ```

* Run code in `tensorflow/structured/base/trainer/` location using the `config.yaml` in this folder.

**Note:** These instructions are used for local testing. When you submit a training job, no code will be executed on 
your local machine.

### Trainer Template Modules

|File Name| Purpose| Do You Need to Change?
|:---|:---|:---
|[experiment.py](tensorflow/structured/base/trainer/experiment.py) |Includes: 1) Creates RunConfig, and 2) Uses one or more GPUs | **No, unless** you want to change distribution strategy.

### Code

The following sample list the number of GPUs in host and then
configure the correct strategy.

```python
  num_gpus = len([device_name
                  for device_name in tf.contrib.eager.list_devices()
                  if '/device:GPU' in device_name])
  logging.info('%s GPUs are available.', str(num_gpus))
  if num_gpus > 1:
    distribution_strategy = tf.distribute.MirroredStrategy()
    logging.info('MirroredStrategy will be used for training.')
    # Update the batch size
    args.batch_size = int(math.ceil(args.batch_size / num_gpus))
```
