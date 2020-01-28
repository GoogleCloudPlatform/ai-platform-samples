from locust import HttpLocust, TaskSet, task, constant_pacing
from locust.clients import HttpSession
import google.auth
from google.auth.transport.requests import Request as goog_request
from requests.auth import AuthBase
from urllib.parse import urlparse
from google.cloud.storage.client import Client as GCSClient
from io import BytesIO
import re
import json
import os
import random
import logging

API_SCOPES = [
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/cloud-platform.read-only'
]
QPS = 1
GCS_HOST = 'https://storage.googleapis.com'
MODEL_URI = 'https://ml.googleapis.com/v1/projects/{}/models/{}{}:predict'
VERSION_ADDON = '/versions/{}'
GCS_CONFIG_PATH_KEY = 'CONFIG_URI'

class SimpleOAuth2(AuthBase):
    def __init__(self, goog_creds, *args, **kwargs):
        super(SimpleOAuth2, self).__init__(*args, **kwargs)
        self.credentials = goog_creds
        self._refresh_token()

    def _refresh_token(self):
        logging.info("Refreshing token...")
        request = goog_request()
        self.credentials.refresh(request)

    def __call__(self, request):
        if self.credentials.expired:
            self._refresh_token()
        self.credentials.apply(request.headers)
        return request

class OAuth2Locust(HttpLocust):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(OAuth2Locust, self).__init__(*args, **kwargs)

        credentials, project_id = google.auth.default(scopes=API_SCOPES)
        auth = SimpleOAuth2(credentials)
        self.client = HttpSession(base_url='')
        self.client.auth = auth

class CloudAITaskSet(TaskSet):
    @task
    def query_model(self):
        self._set_target()
        self.client.post(
            self.model_uri,
            json=self.example
        )

    def _get_model_uri(self, model_cfg):
        v_str = VERSION_ADDON.format(model_cfg['versionId']) if 'versionId' in model_cfg else ''
        m_uri = MODEL_URI.format(
            model_cfg['projectId'],
            model_cfg['modelId'],
            v_str
        )
        return m_uri

    def _get_test_example(self, model_cfg):
        return random.choice(model_cfg['testExamples'])

    def _set_target(self):
        if not (hasattr(self, "model_uri") and hasattr(self, "example")):
            model_cfg = self.locust.model_config
            self.model_uri = self._get_model_uri(model_cfg)
            self.example = self._get_test_example(model_cfg)

class CloudAIUser(OAuth2Locust):
    task_set = CloudAITaskSet
    wait_time = constant_pacing(QPS)

    def __init__(self, *args, **kwargs):
        super(CloudAIUser, self).__init__(*args, **kwargs)

    @classmethod
    def _download_gcs_json(cls, file_url):
        parsed_url = urlparse(file_url)
        if parsed_url.scheme == 'gs':
            file_uri = file_url
        else:
            if parsed_url.netloc == GCS_HOST:
                file_uri = "gs:/{}".format(file_path)
            else:
                raise Exception("Host URL is not a Google Cloud Storage URI: {}".format(file_url))

        gcs_client = GCSClient()
        with BytesIO() as json_in:
            gcs_client.download_blob_to_file(
                file_uri,
                json_in
            )
            json_in.seek(0)
            json_string = json_in.read().decode('utf-8')
        return json_string

    def _load_local_json(self, path):
        with open(path, 'r') as json_in:
            json_string = json_in.read()
        return json_string

    @classmethod
    def _get_model_config(cls):
        if GCS_CONFIG_PATH_KEY not in os.environ:
            raise Exception("You must set '{}' env var to the GCS path to the config".format(GCS_CONFIG_PATH_KEY))
        gcs_config = os.environ[GCS_CONFIG_PATH_KEY]
        json_string = cls._download_gcs_json(gcs_config)
        cls.model_config = json.loads(json_string)

    def setup(self):
        self._get_model_config()
