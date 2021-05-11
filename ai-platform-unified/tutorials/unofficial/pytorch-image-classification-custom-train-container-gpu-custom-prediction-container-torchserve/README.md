# PyTorch Image Classification using GPU and TorchServe with Custom Container

### Environment Variables

```
export PROJECT=aiplatform-dev
export BUCKET=aiplatform-dev
export LOCATION=us-central1

echo "PROJECT: ${PROJECT}"
echo "BUCKET: ${BUCKET}"
echo "LOCATION: ${LOCATION}"
```
```
export ML_FRAMEWORK=pytorch
export ML_TASK=img-cls
export TRAIN_TASK=cust-train-cont-gpu
export PRED_TASK=cust-pred-cont-torchserve

echo "ML_FRAMEWORK: ${ML_FRAMEWORK}"
echo "ML_TASK: ${ML_TASK}"
echo "TRAIN_TASK: ${TRAIN_TASK}"
echo "PRED_TASK: ${PRED_TASK}"
```
```
export TUTORIAL_NAME_TRAIN=${ML_FRAMEWORK}-${ML_TASK}-${TRAIN_TASK}
export TUTORIAL_NAME_PRED=${ML_FRAMEWORK}-${ML_TASK}-${PRED_TASK}

echo "TUTORIAL_NAME: ${TUTORIAL_NAME_TRAIN} for training and ${TUTORIAL_NAME_PRED} for prediction"
```
```
export TUTORIAL_DIR=${PWD}

echo "TUTORIAL_DIR: ${TUTORIAL_DIR}"
```

### Trainer Task Local Run
```
cd ${TUTORIAL_DIR}
cd trainer && python task.py --epochs 1
rm -rf data
rm -rf model
```

### Custom PyTorch Container for Training

```
export HOSTNAME=gcr.io
export IMAGE_TRAIN=${TUTORIAL_NAME_TRAIN}
export TAG=latest
export CONTAINER_IMAGE_URI=${HOSTNAME}/${PROJECT}/${IMAGE_TRAIN}:${TAG}

echo "CONTAINER_IMAGE_URI: ${CONTAINER_IMAGE_URI}"
```
```
cd ${TUTORIAL_DIR}
cd trainer && docker build -t ${CONTAINER_IMAGE_URI} -f Dockerfile .
```
```
docker run --rm ${CONTAINER_IMAGE_URI} --epochs 1
```
```
docker push ${CONTAINER_IMAGE_URI}
```
```
gcloud container images list --repository ${HOSTNAME}/${PROJECT}
```

### Launch a Custom Training Job

##### Configs
###### CPU
```
export CUST_TRAIN_DISPLAY_NAME_SDK=${TUTORIAL_NAME_TRAIN}-sdk-cpu

export MACHINE_TYPE=n1-standard-4
export ACCELERATOR_TYPE=ACCELERATOR_TYPE_UNSPECIFIED
export ACCELERATOR_COUNT=0
export CONT_ARGS="--batch-size 4 --epochs 5"

```

###### Single GPU
```
export CUST_TRAIN_DISPLAY_NAME_SDK=${TUTORIAL_NAME_TRAIN}-sdk-gpu

export MACHINE_TYPE=n1-standard-4
export ACCELERATOR_TYPE=NVIDIA_TESLA_K80
export ACCELERATOR_COUNT=1
export CONT_ARGS="--batch-size 4 --epochs 5"
```

###### Multiple GPUs
```
export CUST_TRAIN_DISPLAY_NAME_SDK=${TUTORIAL_NAME_TRAIN}-sdk-gpus

export MACHINE_TYPE=n1-standard-32
export ACCELERATOR_TYPE=NVIDIA_TESLA_P100
export ACCELERATOR_COUNT=4
export CONT_ARGS="--batch-size 32 --epochs 5"
```

##### SDK
```
echo "CUST_TRAIN_DISPLAY_NAME_SDK: ${CUST_TRAIN_DISPLAY_NAME_SDK}"

echo "MACHINE_TYPE: ${MACHINE_TYPE}"
echo "ACCELERATOR_COUNT: ${ACCELERATOR_COUNT}"
echo "ACCELERATOR_TYPE: ${ACCELERATOR_TYPE}"
echo "CONT_ARGS: ${CONT_ARGS} --epochs 5"

cd ${TUTORIAL_DIR}
python sdk_custom_container_training.py \
    --project ${PROJECT} \
    --bucket ${BUCKET} \
    --location ${LOCATION} \
    --display-name ${CUST_TRAIN_DISPLAY_NAME_SDK} \
    --container-image-uri ${CONTAINER_IMAGE_URI} \
    --machine-type ${MACHINE_TYPE} \
    --accelerator-type ${ACCELERATOR_TYPE} \
    --accelerator-count ${ACCELERATOR_COUNT} \
    --container-args ${CONT_ARGS}
```
###### Output Model Artifact
```
gsutil ls gs://${BUCKET}/${CUST_TRAIN_DISPLAY_NAME_SDK}
```


### Model Archive for TorchServe

```
cd ${TUTORIAL_DIR}
cd model_server && gsutil cp -r gs://${BUCKET}/${CUST_TRAIN_DISPLAY_NAME_SDK}/model .
```
```
cd ${TUTORIAL_DIR}
cd model_server && torch-model-archiver \
     --model-name antandbee \
     --version 1.0 \
     --serialized-file ./model/antandbee.pth \
     --model-file ./model.py \
     --handler ./handler.py \
     --extra-files ./index_to_name.json \
     -f
```
### TorchServe Local Run
```
cd ${TUTORIAL_DIR}
cd model_server && torchserve \
    --model-store ./ \
    --ts-config ./config.properties \
    --models antandbee=antandbee.mar
```

```
curl http://localhost:8080/ping
curl http://127.0.0.1:8081/models/antandbee

wget https://raw.githubusercontent.com/alvarobartt/pytorch-model-serving/master/images/sample.jpg

python convert_b64.py

curl -X POST \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @sample_b64.json \
  http://localhost:8080/predictions/antandbee

```
```
torchserve --stop
rm antandbee.mar
rm -rf logs
```

### Custom TorchServe Container for Prediction

```
export HOSTNAME=gcr.io
export IMAGE_PRED=${TUTORIAL_NAME_PRED}
export TAG=latest
export MODEL_SERVING_CONTAINER_IMAGE_URI=${HOSTNAME}/${PROJECT}/${IMAGE_PRED}:${TAG}

echo "MODEL_SERVING_CONTAINER_IMAGE_URI: ${MODEL_SERVING_CONTAINER_IMAGE_URI}"
```
```
cd ${TUTORIAL_DIR}
cd model_server && docker build -t ${MODEL_SERVING_CONTAINER_IMAGE_URI} -f Dockerfile .
```
```
docker run \
    --rm -it \
    -d \
    --name ts_antandbee \
    -p 8080:8080 \
    -p 8081:8081 \
    ${MODEL_SERVING_CONTAINER_IMAGE_URI} \

curl http://localhost:8080/ping
curl http://127.0.0.1:8081/models/antandbee
```
```
curl -X POST \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @sample_b64.json \
  localhost:8080/predictions/antandbee
```
```
docker stop ts_antandbee
rm sample.jpg
rm sample_b64.json
```
```
docker push ${MODEL_SERVING_CONTAINER_IMAGE_URI}
```
```
gcloud container images list --repository ${HOSTNAME}/${PROJECT}
```


```
export CUST_PRED_DISPLAY_NAME_SDK=${TUTORIAL_NAME_PRED}-sdk
echo "CUST_PRED_DISPLAY_NAME_SDK: ${CUST_PRED_DISPLAY_NAME_SDK}"

```
```
cd ${TUTORIAL_DIR}
python sdk_model_serving.py \
    --project ${PROJECT} \
    --location ${LOCATION} \
    --display-name ${CUST_PRED_DISPLAY_NAME_SDK} \
    --model-serving-container-image-uri ${MODEL_SERVING_CONTAINER_IMAGE_URI}
```
```
cd ${TUTORIAL_DIR}
wget https://raw.githubusercontent.com/alvarobartt/pytorch-model-serving/master/images/sample.jpg
python sdk_online_predict.py \
    --project ${PROJECT} \
    --location ${LOCATION} \
    --endpoint-name projects/430405462454/locations/us-central1/endpoints/7928534367427624960 \
    --image-file-name sample.jpg
rm sample.jpg
```