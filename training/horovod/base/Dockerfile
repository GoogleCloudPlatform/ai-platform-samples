FROM gcr.io/deeplearning-platform-release/tf-gpu

# Install OpenSSH, CUDA, OpenMPI, and NCCL
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends --allow-change-held-packages \
        openssh-client openssh-server openmpi-bin cuda-toolkit-10-0 libopenmpi-dev libnccl2 libnccl-dev

# Install Horovod, temporarily using CUDA stubs
RUN ldconfig /usr/local/cuda/targets/x86_64-linux/lib && \
    HOROVOD_GPU_ALLREDUCE=NCCL HOROVOD_GPU_BROADCAST=NCCL HOROVOD_WITH_TENSORFLOW=1 \
         pip install --no-cache-dir horovod && \
    ldconfig

# Allow OpenSSH to talk to containers without asking for confirmation
RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new && \
    echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new && \
    mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config

# Create SSH key.
RUN mkdir -p /root/.ssh/ && \
    mkdir -p /var/run/sshd && \
    ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

WORKDIR /infra

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
