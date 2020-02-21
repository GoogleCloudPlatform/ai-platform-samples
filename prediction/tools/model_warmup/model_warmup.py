#
# Copyright 2020 Google LLC
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
"""Generate Warmup requests."""

import tensorflow as tf
import requests

from tensorflow.python.framework import tensor_util
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_log_pb2


IMAGE_URL = 'https://tensorflow.org/images/blogs/serving/cat.jpg'
NUM_RECORDS = 100


def get_image_bytes():
    image_content = requests.get(IMAGE_URL, stream=True)
    image_content.raise_for_status()
    return image_content.content
    

def main():
    """Generate TFRecords for warming up."""

    with tf.io.TFRecordWriter("tf_serving_warmup_requests") as writer:
        image_bytes = get_image_bytes()
        predict_request = predict_pb2.PredictRequest()
        predict_request.model_spec.name = 'resnet'
        predict_request.model_spec.signature_name = 'serving_default'
        predict_request.inputs['image_bytes'].CopyFrom(
            tensor_util.make_tensor_proto([image_bytes], tf.string))        
        log = prediction_log_pb2.PredictionLog(
            predict_log=prediction_log_pb2.PredictLog(request=predict_request))
        for r in range(NUM_RECORDS):
            writer.write(log.SerializeToString())        


if __name__ == "__main__":
    main()
