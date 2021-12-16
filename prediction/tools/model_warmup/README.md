# Model warmup

From TensorFlow Serving [documentation](https://www.tensorflow.org/tfx/serving/saved_model_warmup):

> The TensorFlow runtime has components that are lazily initialized, which can cause high latency for the first request/s sent to a model after it is loaded. This latency can be several orders of magnitude higher than that of a single inference request. To reduce the impact of lazy initialization on request latency, it’s possible to trigger the initialization of the sub-systems and components at model load time by providing a sample set of inference requests along with the SavedModel. This process is known as “warming up” the model.

When you deploy a TensorFlow model you may see this message during TensorFlow serving initialization:

```
2020–01–23 23:58:40.355818: I tensorflow_serving/servables/tensorflow/saved_model_warmup.cc:105] No warmup data file found at /models/resnet/1538687457/assets.extra/tf_serving_warmup_requests
```
**Note:** This document can be used in AI Platform prediction during model creation.

For this example, we are deploying a [ResNet50v2](https://github.com/tensorflow/models/tree/main/official/r1/resnet) model for CPU

1. Download model

```
mkdir /tmp/resnet
curl -s http://download.tensorflow.org/models/official/20181001_resnet/savedmodels/resnet_v2_fp32_savedmodel_NHWC_jpg.tar.gz | tar — strip-components=2 -C /tmp/resnet -xvz
ls /tmp/resnet/*
saved_model.pb variables
```

2. Verify model using `saved_model_cli` utility:

```
saved_model_cli show --dir /tmp/resnet/1538687457 --allMetaGraphDef with tag-set: 'serve' contains the following SignatureDefs:

signature_def['predict']:
  The given SavedModel SignatureDef contains the following input(s):
    inputs['image_bytes'] tensor_info:
        dtype: DT_STRING
        shape: (-1)
        name: input_tensor:0
  The given SavedModel SignatureDef contains the following output(s):
    outputs['classes'] tensor_info:
        dtype: DT_INT64
        shape: (-1)
        name: ArgMax:0
    outputs['probabilities'] tensor_info:
        dtype: DT_FLOAT
        shape: (-1, 1001)
        name: softmax_tensor:0
  Method name is: tensorflow/serving/predict

signature_def['serving_default']:
  The given SavedModel SignatureDef contains the following input(s):
    inputs['image_bytes'] tensor_info:
        dtype: DT_STRING
        shape: (-1)
        name: input_tensor:0
  The given SavedModel SignatureDef contains the following output(s):
    outputs['classes'] tensor_info:
        dtype: DT_INT64
        shape: (-1)
        name: ArgMax:0
    outputs['probabilities'] tensor_info:
        dtype: DT_FLOAT
        shape: (-1, 1001)
        name: softmax_tensor:0
  Method name is: tensorflow/serving/predict
```

3. Run the Docker container

```
docker run -p 8501:8501 --mount type=bind,source=/tmp/resnet/,target=/models/resnet -e MODEL_NAME=resnet --rm -i -t tensorflow/serving:latest
```

Output

```
2020–01–23 23:58:38.999634: I tensorflow_serving/model_servers/server.cc:86] Building single TensorFlow model file config: model_name: resnet model_base_path: /models/resnet
2020–01–23 23:58:39.000054: I tensorflow_serving/model_servers/server_core.cc:462] Adding/updating models.
2020–01–23 23:58:39.000131: I tensorflow_serving/model_servers/server_core.cc:573] (Re-)adding model: resnet
2020–01–23 23:58:39.135271: I tensorflow_serving/core/basic_manager.cc:739] Successfully reserved resources to load servable {name: resnet version: 1538687457}
2020–01–23 23:58:39.135365: I tensorflow_serving/core/loader_harness.cc:66] Approving load for servable version {name: resnet version: 1538687457}
2020–01–23 23:58:39.135419: I tensorflow_serving/core/loader_harness.cc:74] Loading servable version {name: resnet version: 1538687457}
2020–01–23 23:58:39.136079: I external/org_tensorflow/tensorflow/cc/saved_model/reader.cc:31] Reading SavedModel from: /models/resnet/1538687457
2020–01–23 23:58:39.151130: I external/org_tensorflow/tensorflow/cc/saved_model/reader.cc:54] Reading meta graph with tags { serve }
2020–01–23 23:58:39.151230: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:264] Reading SavedModel debug info (if present) from: /models/resnet/1538687457
2020–01–23 23:58:39.152541: I external/org_tensorflow/tensorflow/core/platform/cpu_feature_guard.cc:142] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
2020–01–23 23:58:39.244208: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:203] Restoring SavedModel bundle.
2020–01–23 23:58:40.319685: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:152] Running initialization op on SavedModel bundle at path: /models/resnet/1538687457
2020–01–23 23:58:40.350975: I external/org_tensorflow/tensorflow/cc/saved_model/loader.cc:333] SavedModel load for tags { serve }; Status: success: OK. Took 1214904 microseconds.
2020–01–23 23:58:40.355818: I tensorflow_serving/servables/tensorflow/saved_model_warmup.cc:105] No warmup data file found at /models/resnet/1538687457/assets.extra/tf_serving_warmup_requests
2020–01–23 23:58:40.372651: I tensorflow_serving/core/loader_harness.cc:87] Successfully loaded servable version {name: resnet version: 1538687457}
2020–01–23 23:58:40.375813: I tensorflow_serving/model_servers/server.cc:358] Running gRPC ModelServer at 0.0.0.0:8500 …
[warn] getaddrinfo: address family for nodename not supported
2020–01–23 23:58:40.377969: I tensorflow_serving/model_servers/server.cc:378] Exporting HTTP/REST API at:localhost:8501 …
[evhttp_server.cc : 238] NET_LOG: Entering the event loop …
```

4. Take a look at this message:

```
No warmup data file found at /models/resnet/1538687457/assets.extra/tf_serving_warmup_requests
```

5. Generate a warmup request file:

Use [this Python script](model_warmup.py) to generate a warmup file which is relevant to this specific model and inference data.

Script will create a new file called: `tf_serving_warmup_requests`

Move this file to `/tmp/resnet/1538687457/assets.extra/` and then
restart the docker image:

```
mkdir -p /tmp/resnet/1538687457/assets.extra/
cp tf_serving_warmup_requests /tmp/resnet/1538687457/assets.extra/
```

1. Re-run the Docker container. Now, you should see logs showing
   TensorFlow serving reading the warmup data:

```
docker run -p 8500:8500 -p 8501:8501 --mount type=bind,source=/tmp/resnet/,target=/models/resnet -e MODEL_NAME=resnet --rm -i -t tensorflow/serving:latest
```

Output

```
2020–01–24 00:39:40.842570: I tensorflow_serving/servables/tensorflow/saved_model_warmup.cc:117] Starting to read warmup data for model at /models/resnet/1538687457/assets.extra/tf_serving_warmup_requests with model-warmup-options
2020–01–24 00:39:48.485956: I tensorflow_serving/servables/tensorflow/saved_model_warmup.cc:166] Finished reading warmup data for model at /models/resnet/1538687457/assets.extra/tf_serving_warmup_requests. Number of warmup records read: 100. Elapsed time (microseconds): 7646776.
```

You can see now the 100 records being read in 7.6 seconds.

Now when you start sending Prediction requests, initial time should
reduce.