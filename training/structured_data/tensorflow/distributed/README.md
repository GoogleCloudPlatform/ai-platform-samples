# AI Platform Training

## TensorFlow distributed training

TensorFlow's Estimator API parses the TF_CONFIG environment variable,
if present, and uses the relevant details from TF_CONFIG to construct properties
for distributed training, including the cluster spec, task ID, and other
properties.

If your application uses tf.estimator for distributed training, the propagation
of properties to the cluster spec works automatically, as AI Platform sets
TF_CONFIG for you.

Similarly, if you run your distributed training application on AI Platform with
a custom container, then AI Platform sets TF_CONFIG and populates an environment
variable, CLUSTER_SPEC, on each machine.


## Documentation

Please go to the official AI platform [documentation](https://cloud.google.com/ml-engine/docs/tensorflow/distributed-training-details) for more details.
