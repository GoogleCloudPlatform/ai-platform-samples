
This directory holds AI Platform Pipelines example notebooks.

- [pipelines_intro_kfp.ipynb](./pipelines_intro_kfp.ipynb) introduces some of the AI Platform Pipelines features, using the [Kubeflow Pipelines (KFP) SDK](https://www.kubeflow.org/docs/components/pipelines/).
- [control_flow_kfp.ipynb](./control_flow_kfp.ipynb) shows how you can build pipelines that include conditionals and parallel 'for' loops using the KFP SDK.
- [lightweight_functions_component_io_kfp.ipynb](./lightweight_functions_component_io_kfp.ipynb) shows how to build lightweight Python function-based components, and in particular how to support component I/O using the KFP SDK.
- [metrics_viz_run_compare_kfp](./metrics_viz_run_compare_kfp) shows how to use the KFP SDK to build AI Platform Pipelines that generate model metrics and metrics visualizations; and how to compare pipeline runs.

The following examples show how to use the components defined in [google_cloud_pipeline_components](https://github.com/kubeflow/pipelines/tree/master/components/google-cloud) to build pipelines that access AI Platform (Unified) services.

- [google-cloud-pipeline-components_automl_images.ipynb](./google-cloud-pipeline-components_automl_images.ipynb)
- [google-cloud-pipeline-components_automl_tabular.ipynb](./google-cloud-pipeline-components_automl_tabular.ipynb)
- [google-cloud-pipeline-components_automl_text.ipynb](./google-cloud-pipeline-components_automl_text.ipynb)
- (Experimental) [google_cloud_pipeline_components_model_train_upload_deploy.ipynb](./google_cloud_pipeline_components_model_train_upload_deploy.ipynb): includes an experimental component to run a custom training job directly by defining its worker specs
