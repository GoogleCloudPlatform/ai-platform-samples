FROM horovod-wrapper:latest

ARG GCS_OUTPUT_PATH
ARG STAGE_GCS_PATH 
# Set these environment variables to copy input files from GCS.
ENV STAGE_GCS_PATH ${STAGE_GCS_PATH}
# Set these environment variables to copy output files to GCS.
ENV GCS_OUTPUT_PATH ${GCS_OUTPUT_PATH}

WORKDIR /infra

# Download examples
RUN git clone --depth 1 https://github.com/horovod/horovod.git && \
    mv horovod/examples . && rm -rf horovod

WORKDIR /output

CMD ["python", "/infra/examples/keras/keras_mnist.py"]
