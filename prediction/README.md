# AI Platform Prediction

You can host your trained machine learning models in the cloud and use the Cloud ML prediction service to infer target values for new data. This page discusses model hosting and prediction and introduces considerations you should keep in mind for your projects.
How it works

The AI Platform prediction service manages computing resources in the cloud to run your models. You can request predictions from your models and get predicted target values for them. Here is the process to get set up to make predictions in the cloud:

- You export your model as a [SavedModel](https://cloud.google.com/ml-engine/docs/tensorflow/exporting-for-prediction) or as other artifacts to be used in a [custom prediction routine (beta)](https://cloud.google.com/ml-engine/docs/tensorflow/custom-prediction-routines).

- You create a model resource in AI Platform and then create a model version from your saved model.

- If you're deploying a custom prediction routine, you also provide the code to run at prediction time.
  Note: You can use batch prediction to get inferences for a SavedModel that isn't deployed to AI Platform.

- You format your input data for prediction and request either online prediction or batch prediction

When you use online prediction, the service runs your saved model and returns the requested predictions as the response message for the call.

Your model version is deployed in the region you specified when you created the model.
Although it is not guaranteed, a model version that you use regularly is generally kept ready to run.

When you use batch prediction, the process is a little more involved:

 - The prediction service allocates resources to run your job. This includes one or more prediction nodes.

 - The service restores your TensorFlow graph on each allocated node.

 - The prediction service distributes your input data across the allocated nodes.

 - Each node runs your graph and saves the predictions to a Cloud Storage location that you specify.

 - When all of your input data is processed, the service shuts down your job and releases the resources it allocated for it.


Documentation
-------------

We host AI Platform Prediction documentation [here](https://cloud.google.com/ml-engine/docs/tensorflow/prediction-overview)
