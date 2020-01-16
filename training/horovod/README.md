# Run Horovod on AI Platform

Download and build Horovod base docker image:
```
git clone https://github.com/horovod/horovod
cd horovod
docker build -t ai-platform-horovod-base --build-arg python=3.6 .
```

Download and build AI Platform wrapper for Horovod:
```
git clone https://github.com/GoogleCloudPlatform/ai-platform-samples
cd ai-platform-samples/training/horovod/base/
docker build -t horovod-wrapper .
```

Now to run TensorPack FasterRCNN example, download TensorPack
```
git clone https://github.com/tensorpack/tensorpack
cd tensorpack/examples/FasterRCNN
```
and create this Dockerfile:

```
FROM horovod-wrapper:latest
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3-opencv

RUN pip install cython tensorpack
RUN pip install git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI
COPY . /examples/
ENV STAGE_GCS_PATH gs://GS_BUCKET_NAME/coco_dataset
ENV TASK_STARTUP_TIMEOUT_SECONDS=1200
CMD ["python", "/examples/train.py", "--config", "DATA.BASEDIR=/input/coco",\
     "TRAINER=horovod", "MODE_FPN=True", "FPN.CASCADE=True", \
     "BACKBONE.RESNET_NUM_BLOCKS=[3,4,23,3]", "FPN.NORM=GN", \
     "BACKBONE.NORM=GN", "FPN.FRCNN_HEAD_FUNC=fastrcnn_4conv1fc_gn_head", \
     "FPN.MRCNN_HEAD_FUNC=maskrcnn_up4conv_gn_head", \
     "PREPROC.TRAIN_SHORT_EDGE_SIZE=[640,800]", "TRAIN.LR_SCHEDULE=9x", \
     "BACKBONE.FREEZE_AT=0"]
```

Then build the docker image and push it gcr.io (make sure gcr.io is enabled here):

```
docker build -t gcr.io/$PROJECT_ID/horovod-fasterrcnn:latest .
docker push gcr.io/$PROJECT_ID/horovod-fasterrcnn:latest
```

Prepare the dataset so that there are the following directories in coco_dataset:

```
  annotations/  train2014/  train2017  val2014/  val2017/
```

Finally to run the trainer on 8 machines with 8 gpus:

```
gcloud ai-platform jobs submit training horovod_fasterrcnn --region=us-west1  --scale-tier=CUSTOM \
--master-image-uri=gcr.io/$PROJECT_ID/horovod-fasterrcnn:latest \
--worker-image-uri=gcr.io/$PROJECT_ID/horovod-fasterrcnn:latest \
--worker-count=7 \
--master-machine-type=n1-standard-64 --master-accelerator count=8,type=nvidia-tesla-v100 \
--worker-machine-type=n1-standard-64 --worker-accelerator count=8,type=nvidia-tesla-v100 
```