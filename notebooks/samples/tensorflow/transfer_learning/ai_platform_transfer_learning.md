```python
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
```

<table align="left">
  <td>
    <a href="https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/templates/ai_platform_notebooks_template.ipynb">
      <img src="https://cloud.google.com/ml-engine/images/colab-logo-32px.png" alt="Colab logo"> Run in Colab
    </a>
  </td>
  <td>
    <a href="https://github.com/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/templates/ai_platform_notebooks_template.ipynb">
      <img src="https://cloud.google.com/ml-engine/images/github-logo-32px.png" alt="GitHub logo">
      View on GitHub
    </a>
  </td>
</table>

# Overview

Modern image recognition models have millions of parameters. Training them from scratch requires a lot of labeled training data and a lot of computing power (hundreds of GPU-hours or more). Transfer learning is a technique that shortcuts much of this by taking a piece of a model that has already been trained on a related task and reusing it in a new model. In this tutorial, we will reuse the feature extraction capabilities from powerful image classifiers trained on ImageNet and simply train a new classification layer on top.

This tutorial uses TensorFlow Hub to share a pre-trained model.
This tutorial demostrates:

1. How to use TensorFlow Hub with tf.keras
2. How to do image classification using TensorFlow Hub
3. How to do simple Transfer learning
4. Save model in AI platform bucket

### Dataset

TensorFlow flowers dataset:

- URL: http://download.tensorflow.org/example_images/flower_photos.tgz
- DatasetBuilder: tfds.image.flowers.TFFlowers
- Version: v1.0.0
- Size: 218.21 MiB

### Objective

Train an image classification model using Transfer Learning; once
model has been trained, save it in AI platform. Use
TF Hub to retrain the top layer of an existing model to recognize the
classes in our dataset.

### Costs

This tutorial uses billable components of Google Cloud Platform (GCP):

* Cloud AI Platform
* Cloud Storage

Learn about [Cloud AI Platform
pricing](https://cloud.google.com/ml-engine/docs/pricing) and [Cloud Storage
pricing](https://cloud.google.com/storage/pricing), and use the [Pricing
Calculator](https://cloud.google.com/products/calculator/)
to generate a cost estimate based on your projected usage.

## PIP Install Packages and dependencies

Install additional dependencies not installed in Notebook environment
(e.g. XGBoost, adanet, tf-hub)


```python
! pip install --upgrade pip
! pip install -U tensorflow_hub
```


```python
# Automatically restart kernel after installs
import IPython
app = IPython.Application.instance()
app.kernel.do_shutdown(True)
```

### Set up your GCP project

**The following steps are required, regardless of your notebook environment.**

1. [Select or create a GCP project.](https://console.cloud.google.com/cloud-resource-manager). When you first create an account, you get a $300 free credit towards your compute/storage costs.

2. [Make sure that billing is enabled for your project.](https://cloud.google.com/billing/docs/how-to/modify-project)

3. [Enable the AI Platform APIs and Compute Engine APIs.](https://console.cloud.google.com/flows/enableapi?apiid=ml.googleapis.com,compute_component)

4. [Google Cloud SDK](https://cloud.google.com/sdk) is already installed in AI Platform Notebooks.

5. Enter your project ID in the cell below. Then run the  cell to make sure the
Cloud SDK uses the right project for all the commands in this notebook.

**Note**: Jupyter runs lines prefixed with `!` as shell commands, and it interpolates Python variables prefixed with `$` into these commands.


```python
# TODO (Set your GCP project name)
PROJECT_ID = "[your-project-id]" #@param {type:"string"}
! gcloud config set project $PROJECT_ID
```

### Authenticate your GCP account

**If you are using AI Platform Notebooks**, your environment is already
authenticated. Skip this step.

**If you are using Colab**, run the cell below and follow the instructions
when prompted to authenticate your account via oAuth.

**Otherwise**, follow these steps:

1. In the GCP Console, go to the [**Create service account key**
   page](https://console.cloud.google.com/apis/credentials/serviceaccountkey).

2. From the **Service account** drop-down list, select **New service account**.

3. In the **Service account name** field, enter a name.

4. From the **Role** drop-down list, select
   **Machine Learning Engine > AI Platform Admin** and
   **Storage > Storage Object Admin**.

5. Click *Create*. A JSON file that contains your key downloads to your
local environment.

6. Enter the path to your service account key as the
`GOOGLE_APPLICATION_CREDENTIALS` variable in the cell below and run the cell.

If you are running this notebook in Colab, run the following cell to authenticate your Google Cloud Platform user account


```python
import sys

# If you are running this notebook in Colab, run this cell and follow the
# instructions to authenticate your GCP account. This provides access to your
# Cloud Storage bucket and lets you submit training jobs and prediction
# requests.

if 'google.colab' in sys.modules:
  from google.colab import auth as google_auth
  google_auth.authenticate_user()

# If you are running this notebook locally, replace the string below with the
# path to your service account key and run this cell to authenticate your GCP
# account.
else:
  %env GOOGLE_APPLICATION_CREDENTIALS ''
```

### Create a Cloud Storage bucket

**The following steps are required, regardless of your notebook environment.**

When you submit a training job using the Cloud SDK, you upload a Python package
containing your training code to a Cloud Storage bucket. AI Platform runs
the code from this package. In this tutorial, AI Platform also saves the
trained model that results from your job in the same bucket. You can then
create an AI Platform model version based on this output in order to serve
online predictions.

Set the name of your Cloud Storage bucket below. It must be unique across all
Cloud Storage buckets.

You may also change the `REGION` variable, which is used for operations
throughout the rest of this notebook. Make sure to [choose a region where Cloud
AI Platform services are
available](https://cloud.google.com/ml-engine/docs/tensorflow/regions). You may
not use a Multi-Regional Storage bucket for training with AI Platform.


```python
# TODO (Set your bucket name)
BUCKET_NAME = "[your-bucket-name]" #@param {type:"string"}

# TODO (Set your region)
REGION = "[your-region]" #@param {type:"string"}
```

**Only if your bucket doesn't already exist**: Run the following cell to create your Cloud Storage bucket.


```python
! gsutil mb -l $REGION gs://$BUCKET_NAME
```

Finally, validate access to your Cloud Storage bucket by examining its contents:


```python
! gsutil ls -al gs://$BUCKET_NAME
```

### Import libraries and define constants


```python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib.pylab as plt
import numpy as np
import os

import tensorflow as tf
import tensorflow_hub as hub

from tensorflow.keras import layers
```

## 1. Obtaining a training dataset

For this example, you will be using the Tensorflow flowers dataset:


```python
data_root = tf.keras.utils.get_file(
  'flower_photos','https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
   untar=True)
```


```python
# Verify folder structure:
! ls -al {data_root}
```

The simplest way to load this data into our model is using [`tf.keras.preprocessing.image.ImageDataGenerator`](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html),

All of TensorFlow Hub's image modules expect float inputs in the [0, 1] range. Use the ImageDataGenerator's rescale parameter to achieve this. The image size will be handled later.


```python
# Image information
HEIGHT = 224
WIDTH = 224
CHANNELS = 3
IMAGE_SHAPE = (HEIGHT, WIDTH)
```


```python
image_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1/255)
image_data = image_generator.flow_from_directory(str(data_root), target_size=IMAGE_SHAPE)
```

The resulting object is an iterator that returns:
 - `image_batch, label_batch` pairs.


```python
for image_batch, label_batch in image_data:
  print("Image batch shape: ", image_batch.shape)
  print("Label batch shape: ", label_batch.shape)
  break
```

## 2. Download the headless model

TensorFlow Hub also distributes models without the top classification layer. These can be used to easily do transfer learning.

Any [TensorFlow 2.x image feature vector URL](https://tfhub.dev/s?module-type=image-feature-vector&tf-version=tf2) from tfhub.dev will work here.


```python
# TODO: replace the URL with any TF 2.x image feature vector from tfhub.dev
feature_extractor_url = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4" #@param {type:"string"}
```

Create the layer, and check the expected image size:


```python
feature_extractor_layer = hub.KerasLayer(feature_extractor_url,
                                         input_shape=(HEIGHT, WIDTH, CHANNELS))
feature_batch = feature_extractor_layer(image_batch)
print(feature_batch.shape)
```

The feature extractor returns a 1280-element vector for each image.

Freeze the variables in the feature extractor layer, so that the training only modifies the new classifier layer.


```python
feature_extractor_layer.trainable = False
```

## 3. Attach a classification head

Now wrap the hub layer in a tf.keras.Sequential model, and add a new classification layer.


```python
model = tf.keras.Sequential([
  feature_extractor_layer,
  layers.Dense(image_data.num_classes, activation='softmax')
])

model.summary()
```


```python
predictions = model(image_batch)
predictions.shape
```

## 4. Train the model

Use compile to configure the training process:


```python
model.compile(
  optimizer=tf.keras.optimizers.Adam(),
  loss='categorical_crossentropy',
  metrics=['acc'])
```

Now use the .fit method to train the model.

To keep this example short, train just 5 epochs. To visualize the training progress, use a custom callback to log the loss and accuracy of each batch individually, instead of the epoch average.


```python
class CollectBatchStats(tf.keras.callbacks.Callback):
  def __init__(self):
    self.batch_losses = []
    self.batch_acc = []

  def on_train_batch_end(self, batch, logs=None):
    self.batch_losses.append(logs['loss'])
    self.batch_acc.append(logs['acc'])
    self.model.reset_metrics()
```


```python
steps_per_epoch = np.ceil(image_data.samples/image_data.batch_size)
batch_stats_callback = CollectBatchStats()

history = model.fit(image_data, epochs=5,
                    steps_per_epoch=steps_per_epoch,
                    callbacks = [batch_stats_callback])
```

Now after, even just a few training iterations, we can already see that the model is making progress on the task.


```python
# Plotting loss
plt.figure()
plt.ylabel("Loss")
plt.xlabel("Training Steps")
plt.ylim([0,2])
plt.plot(batch_stats_callback.batch_losses)
```


```python
# Plotting accuracy
plt.figure()
plt.ylabel("Accuracy")
plt.xlabel("Training Steps")
plt.ylim([0,1])
plt.plot(batch_stats_callback.batch_acc)
```

## 5. Check the predictions

To redo the plot from before, first get the ordered list of class names:


```python
class_names = sorted(image_data.class_indices.items(), key=lambda pair:pair[1])
class_names = np.array([key.title() for key, value in class_names])
class_names
```

Run the image batch through the model and convert the indices to class names.


```python
predicted_batch = model.predict(image_batch)
predicted_id = np.argmax(predicted_batch, axis=-1)
predicted_label_batch = class_names[predicted_id]
```

Plot the result:


```python
label_id = np.argmax(label_batch, axis=-1)
plt.figure(figsize=(10, 9))
plt.subplots_adjust(hspace=0.5)
for n in range(30):
  plt.subplot(6, 5, n+1)
  plt.imshow(image_batch[n])
  color = "green" if predicted_id[n] == label_id[n] else "red"
  plt.title(predicted_label_batch[n].title(), color=color)
  plt.axis('off')
_ = plt.suptitle("Model predictions (green: correct, red: incorrect)")
```

## 6. Save your model

Now that you've trained the model, save it in "tf" format (this is the default format for TF 2.x). Export the model to user defined bucket.


```python
# TODO: label version as needed
VERSION = 1565292863

tf_export_path = "gs://{}/saved_models/{}".format(BUCKET_NAME, VERSION)
tf.keras.models.save_model(model,
                           tf_export_path,
                           include_optimizer=True,
                           save_format="tf")

# Print directory where model is located
tf_export_path
```

Verify that the model has been saved successfully:


```python
# TODO (Set your bucket and version)
! gsutil ls -l "gs://[your-bucket-name]/saved_models/[your-version-name]/"
```

# Cleaning up

To clean up all GCP resources used in this project, you can [delete the GCP
project](https://cloud.google.com/resource-manager/docs/creating-managing-projects#shutting_down_projects) you used for the tutorial.

{Include commands to delete individual resources below}


```python
# Delete model from bucket
# TODO (Set your bucket and version)
! gsutil rm "gs://[your-bucket-name]/saved_models/[your-version-name]/"
```

