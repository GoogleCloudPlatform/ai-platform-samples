FROM horovod-wrapper:latest

ARG GCS_OUTPUT_PATH
ARG STAGE_GCS_PATH 
# Set these environment variables to copy input files from GCS.
ENV STAGE_GCS_PATH ${STAGE_GCS_PATH}
# Set these environment variables to copy output files to GCS.
ENV GCS_OUTPUT_PATH ${GCS_OUTPUT_PATH}

RUN git clone https://github.com/tensorpack/tensorpack && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends --allow-change-held-packages \
        python3-opencv && \
    pip install cython git+https://github.com/tensorpack/tensorpack.git && \
    pip install git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI

# Staging from GCS takes a long time so extend the timeout limit
ENV TASK_STARTUP_TIMEOUT_SECONDS=3600

ENV TF_CUDNN_USE_AUTOTUNE=0

WORKDIR /output

CMD ["python", "/infra/tensorpack/examples/FasterRCNN/train.py", \
     "--config", "DATA.BASEDIR=/input", \
     "BACKBONE.WEIGHTS=/input/ImageNet-R50-AlignPadding.npz", \
     "TRAINER=horovod"]