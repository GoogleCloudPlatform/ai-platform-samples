FROM locustio/locust
RUN pip3 install --user --upgrade \
  google-cloud-storage \
  google-api-python-client

COPY locustfile.py /

ENV TARGET_URL https://ml.googleapis.com
