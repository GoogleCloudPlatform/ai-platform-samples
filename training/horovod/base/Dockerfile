FROM ai-platform-horovod-base

ARG CLOUD_SDK_VERSION=240.0.0
ENV CLOUD_SDK_VERSION=$CLOUD_SDK_VERSION

RUN apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends wget python2.7

# Installs google cloud sdk, this is mostly for using gsutil to export model.
RUN wget -nv \
    https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz && \
    mkdir /root/tools && \
    tar xvzf google-cloud-sdk.tar.gz -C /root/tools && \
    rm google-cloud-sdk.tar.gz && \
    /root/tools/google-cloud-sdk/install.sh --usage-reporting=false \
        --path-update=false --bash-completion=false \
        --disable-installation-options && \
    rm -rf /root/.config/* && \
    ln -s /root/.config /config && \
    # Remove the backup directory that gcloud creates
    rm -rf /root/tools/google-cloud-sdk/.install/.backup

RUN pip install pandas google-cloud-storage
# Install newer version of horovod to avoid segfaults:
# https://github.com/horovod/horovod/issues/1232
RUN pip uninstall -y horovod
RUN HOROVOD_GPU_ALLREDUCE=NCCL HOROVOD_WITH_TENSORFLOW=1 \
    pip install --no-cache-dir git+https://github.com/horovod/horovod

ENV PATH $PATH:/root/tools/google-cloud-sdk/bin
ENV LD_LIBRARY_PATH /usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH "${LD_LIBRARY_PATH}:/usr/local/nvidia/lib:/usr/local/nvidia/lib64"
# Make sure gsutil will use the default service account
RUN echo '[GoogleCompute]\nservice_account = default' > /etc/boto.cfg

# Create SSH key.
RUN mkdir -p /root/.ssh/ && \
    mkdir -p /var/run/sshd && \
    ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys
WORKDIR /infra
ENV LD_LIBRARY_PATH /usr/local/cuda/extras/CUPTI/lib64:$LD_LIBRARY_PATH

# Use along with
# ENV GCS_OUTPUT_PATH gs://path
# to copy gs://path to /output
ENV OUTPUT_DIR /output/
EXPOSE 2222

COPY horovod_wrapper.py /infra

# Use along with ENV STAGE_GCS_PATH gs://path to copy gs://path to /output
ENV STAGING_DIR /input

# For local run only
ENV TF_CONFIG '{"cluster":{"master":["127.0.0.1:2222"]}, "task":{"type":"master","index":0}}'

ENTRYPOINT ["python", "/infra/horovod_wrapper.py"]
