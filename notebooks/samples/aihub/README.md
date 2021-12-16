# AI Hub ML Container Examples

This folder holds notebooks with examples of using [ML Containers from the AI Hub](https://aihub.cloud.google.com/u/0/s?category=ml-container).

The notebooks show an example workflow of:
- create a dataset
- train an ML model
- monitor the training
- validate the trained model
- deploy the trained model for serving
- get online predictions
- interactively examine the model with the What-if Tool

## ML Containers

| AI Hub documentation | GitHub preview | Colab Notebook |
| --- | --- | --- |
| [PCA](https://aihub.cloud.google.com/u/0/p/products%2Fcd31a10b-85db-4c78-830c-a3794dd606ce) | [Dimensionality reduction](pca/pca.ipynb) | [Dimensionality reduction](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/pca/pca.ipynb)
| [K-Means](https://aihub.cloud.google.com/u/0/p/products%2F0e0d2ed0-5563-4639-b348-53a83ac4ff4e) | [Clustering](kmeans/kmeans.ipynb) | [K-Means](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/kmeans/kmeans.ipynb) |
| [Factorization Machines](https://aihub.cloud.google.com/u/0/p/products%2F2fdb9ade-17cc-4872-8d30-ca38aab5f071) | [Classification](factorization_machines_classification/factorization_machines_classification.ipynb), [Regression](factorization_machines_regression/factorization_machines_regression.ipynb) | [Classification](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/factorization_machines_classification/factorization_machines_classification.ipynb), [Regression](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/factorization_machines_regression/factorization_machines_regression.ipynb) |
| [Tabular Anomaly Detection](https://aihub.cloud.google.com/u/0/p/products%2F6427563a-f2a8-4f9e-a104-a4dbc95d4e3e) | [Anomaly detection](tabular_anomaly_detection/tabular_anomaly_detection.ipynb) | [Anomaly detection](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/tabular_anomaly_detection/tabular_anomaly_detection.ipynb) |
| [XGBoost](https://aihub.cloud.google.com/u/0/p/products%2F0ccd8a63-71a7-4e48-a68b-685692a62e92) | [Classification](xgboost_classification/xgboost_classification.ipynb), [Regression](xgboost_regression/xgboost_regression.ipynb) | [Classification](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/xgboost_classification/xgboost_classification.ipynb), [Regression](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/xgboost_regression/xgboost_regression.ipynb) |
| [TF Module image](https://aihub.cloud.google.com/u/0/p/products%2F404b6288-7a92-42d2-869d-862df6cba931) | [Image classification](tf_module_image/tf_module_image.ipynb) | [Image classification](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/tf_module_image/tf_module_image.ipynb) |
| [ResNet](https://aihub.cloud.google.com/u/0/p/products%2F4b08be38-7a6c-41b8-9d13-bfaa11cf199f) | [Image classification](resnet/resnet.ipynb) | [Image classification](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/retinanet/retinanet.ipynb) |
| [RetinaNet](https://aihub.cloud.google.com/u/0/p/products%2F5ab1b26d-9d4a-44c7-8dbc-365d4d5233f3) | [Object detection in image](retinanet/retinanet.ipynb) | [Object detection in image](https://colab.research.google.com/github/post2web/aihub-ml-container-examples/blob/master/notebooks/retinanet.ipynb) |
| [Tabular Data Inspection](https://aihub.cloud.google.com/u/0/p/products%2F19b6a156-3ede-47de-9aa4-ace6b351849b) |  [Visualize data statistics](tabular_data_inspection/tabular_data_inspection.ipynb) | [Visualize data statistics](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/tabular_data_inspection/tabular_data_inspection.ipynb) |
| [KNN](https://aihub.cloud.google.com/u/0/p/products%2F9d576c4f-e774-4626-b19e-ff5f9dd2d7e6) | [Classification](knn_classification/knn_classification.ipynb), [Regression](knn_regression/knn_regression.ipynb) | [Classification](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/knn_classification/knn_classification.ipynb), [Regression](https://colab.research.google.com/github/GoogleCloudPlatform/ai-platform-samples/blob/main/notebooks/samples/aihub/knn_regression/knn_regression.ipynb) |


Note that all of the ML containers generate an HTML report file (Run Report) that is embedded in the notebooks. GitHub renderers the notebooks in a way that doesn't show JavaScript plots from those reports.

For an example of using those ML Containers with [Kubeflow pipelines](https://www.kubeflow.org/docs/pipelines/overview/pipelines-overview/), [read this article](https://www.linkedin.com/pulse/pipelines-production-ml-systems-ivelin-angelov).

## License

By deploying or using this software you agree to comply with the [AI Hub Terms of Service]( https://aihub.cloud.google.com/u/0/aihub-tos) and the [Google APIs Terms of Service](https://developers.google.com/terms/). To the extent of a direct conflict of terms, the AI Hub Terms of Service will control.