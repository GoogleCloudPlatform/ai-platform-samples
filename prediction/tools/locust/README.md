# Load testing for Cloud AI platform
Easily run a load test on models deployed on Cloud AI Platform from GCE, GKE, or local.

# Features
- Easy to use: Shipped as a complete Docker container. Just pass in some credentials and a file telling your deployment endpoint and you're done! You don't have to understand any of the underlying libraries to get started.
- Scalable: Using Locust.io's native distributed functionality, you can scale up to thousands of requesters.
- Customizable: the container is based on Locust.io and the

# Getting started
The easiest way to get started is to use the Docker container available at [https://gcr.io/htappen-caip/load-test]

0. Deploy a model to Cloud AI Platform. Create a JSON file with information about your model:
```
{
  "projectId": "<your project ID>"
  "modelId": "<your model name>"
  "testExamples": [
    <put a prediction request body>
  ]
}
```
Prediction request body details are available in the [Cloud AI Platform docs](https://cloud.google.com/ml-engine/docs/online-predict)

1. Put the JSON file on Google Cloud Storage. Note the URI for it.
2. Grab the image from [gcr.io](https://gcr.io/htappen-caip/load-test)
3. When you launch the image, make sure you set
    - [Application default credentials](https://cloud.google.com/docs/authentication/production)
    - An environment variable `CONFIG_URI` set to the GCS URI path from step 2
    - If you're running the test [without Locust's UI](https://docs.locust.io/en/stable/running-locust-without-web-ui.html), pass in an env variable `LOCUST_OPTS` with the necessary parameters. You'll definitely want to set `--no-web`, `-c` (number of clients), `-r` (hatch rate) and `-t` (run time). See the next step for the meaning of these arguments.
4. Start the test! Locust will ask you (or you'll specify in the cmd line) the number of clients and the hatch rate. Each client makes ~1 QPS, so the number of clients should be the max QPS you want to simulate. The hatch rate tells the ramp up in QPS, or how many new requesters you want to make each second.

Note: If you're using the web UI, point your browser to port 8089 on the target host.

Want to use more of Locust's options? Pass in the env variable `LOCUST_OPTS` = `--help`, and you'll get a list of all the things Locust supports.

Example:

```
docker run --name locus_loadtest \
    -v /keys/gcp-service-key.json:/config \
    -e GOOGLE_APPLICATION_CREDENTIALS=/config \
    -e LOCUST_OPTS="--clients=2 --no-web --run-time=600" \
    -e CONFIG_URI="gs://<my-bucket>/project.json" \
    -t gcr.io/htappen-caip/load-test
```
