FROM horovod-wrapper:latest

ARG GCS_OUTPUT_PATH
ARG STAGE_GCS_PATH 
# Set these environment variables to copy input files from GCS.
ENV STAGE_GCS_PATH ${STAGE_GCS_PATH}
# Set these environment variables to copy output files to GCS.
ENV GCS_OUTPUT_PATH ${GCS_OUTPUT_PATH}

WORKDIR /infra

# Download examples
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends subversion && \
    svn checkout https://github.com/horovod/horovod/trunk/examples && \
    rm -rf examples/.svn

WORKDIR /output

CMD ["python", "/infra/examples/keras_mnist.py"]
