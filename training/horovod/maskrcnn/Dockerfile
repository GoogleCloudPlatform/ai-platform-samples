FROM horovod-wrapper:latest

ARG GCS_OUTPUT_PATH
ARG STAGE_GCS_PATH 
# Set these environment variables to copy input files from GCS.
ENV STAGE_GCS_PATH ${STAGE_GCS_PATH}
# Set these environment variables to copy output files to GCS.
ENV GCS_OUTPUT_PATH ${GCS_OUTPUT_PATH}

# b/162233627: Uninstall dask to resolve segfaults
RUN pip uninstall -y dask && \
    git clone https://github.com/tensorpack/tensorpack && \
    pip install cython scipy opencv-python==3.4.2.17 \
        ./tensorpack \
        git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI

# Staging from GCS takes a long time so extend the timeout limit
ENV TASK_STARTUP_TIMEOUT_SECONDS=3600
ENV TF_CUDNN_USE_AUTOTUNE=0

WORKDIR /output

CMD ["python", "/infra/tensorpack/examples/FasterRCNN/train.py", \
     "--config", "DATA.BASEDIR=/input", \
     "BACKBONE.WEIGHTS=/input/ImageNet-R50-AlignPadding.npz", \
     "TRAIN.EVAL_PERIOD=0", \
     "TRAIN.LR_SCHEDULE=1x", \
     "TRAINER=horovod"]