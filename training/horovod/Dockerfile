FROM ai-platform-horovod-wrapper
ARG GCS_OUTPUT_PATH
ARG STAGE_GCS_PATH 
# Set these environment variables to copy input files from GCS.
ENV STAGE_GCS_PATH ${STAGE_GCS_PATH}
# ENV STAGING_DIR /input
# Set these environment variables to copy output files to GCS.
ENV GCS_OUTPUT_PATH ${GCS_OUTPUT_PATH}
ENV OUTPUT_DIR /output
WORKDIR /output
CMD ["python", "/examples/keras_mnist.py"]
