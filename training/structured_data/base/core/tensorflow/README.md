# TensorFlow Estimator - Trainer Package

The purpose of this repository is to provide a sample of how you can package a
TensorFlow training model to submit it to AI Platform. The code makes it
easier to organise your code, and to adapt it to your dataset. In more details,
the template covers the following functionality:

*   Metadata to define your dataset, along with the problem type
    (Classification).
*   Standard implementation of input, parsing, and serving functions.
*   Automatic feature columns creation based on the metadata (and normalization
    stats).
*   Wide & Deep model construction using canned estimators.
*   Train, evaluate, and export the model.
*   Parameterization of the experiment.

Although this sample provides standard implementation to different
functionality, you can customise these parts with your own implementation.

### Repository Structure

1.  **[core](core)**: The directory includes: 1) trainer template with all the
    python modules to adapt to your data. 2) `setup.py`. 3) `config.yaml` file
    for hyper-parameter tuning and specifying the AI Platform scale-tier.

2.  **[scripts](scripts)**: The directory includes command-line scripts to: 1)
    Train the model locally. 2) Train the model on AI Platform. 3) Deploy the
    model on GCP as well as to make prediction (inference) using the deployed
    model.

### Dataset

Scripts will look for a data/ folder to contain, you can use `.download_data.sh` to
create folder and download files:
 - nano_taxi_trips_train.csv
 - nano_taxi_trips_eval.csv
 - new-data.json
 - new-data.csv



The examples show how the template is adapted given a dataset. The datasets are
found in the examples' folders (under "data" sub-directory).

### Trainer Template Modules

File Name                                         | Purpose                                                                                                                                                                                                                                                                                                                                | Do You Need to Change?
:------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------
[metadata.py](tensorflow/trainer/metadata.py)     | Defines: 1) task type, 2) input data header, 3) numeric and categorical feature names, and 4) target feature name (and labels, for a classification task)                                                                                                                                                                              | **Yes**, as you will need to specify the metadata of your dataset. **This might be the only module to change!**
[inputs.py](tensorflow/trainer/inputs.py)         | Includes: 1) data input functions to read data from csv and tfrecords files, 2) parsing functions to convert csv and tf.example to tensors, 3) function to implement your custom features processing and creation functionality, and 4) prediction functions (for serving the model) that accepts CSV, JSON, and tf.example instances. | **Maybe**, if you want to implement any custom pre-processing and feature creation during reading data.
[featurizer.py](tensorflow/trainer/featurizer.py) | Creates: 1) TensorFlow feature_column(s) based on the dataset metadata (and other extended feature columns, e.g. bucketisation, crossing, embedding, etc.), and 2) deep and wide feature column lists.                                                                                                                                 | **Maybe**, if you want to change your feature_column(s) and/or change how deep and wide columns are defined.
[model.py](tensorflow/trainer/model.py)           | Includes: 1) function to create DNNLinearCombinedRegressor, and 2) DNNLinearCombinedClassifier.                                                                                                                                                                                                                                        | **No, unless** you want to change something in the estimator, e.g., activation functions, optimizers, etc..
[experiment.py](tensorflow/trainer/task.py)       | Runs the model training and evaluation experiment, and exports the final model.                                                                                                                                                                                                                                                        | **No, unless** you want to add/remove parameters, or change parameter default values.
[task.py](tensorflow/trainer/task.py)             | Includes: 1) Initialise and parse task arguments (hyper parameters), and 2) Entry point to the trainer.                                                                                                                                                                                                                                | **No, unless** you want to add/remove parameters, or change parameter default values.

### Suitable for TensorFlow v1.13.1+
