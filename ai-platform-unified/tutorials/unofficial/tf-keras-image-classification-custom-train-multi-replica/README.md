# Keras Image Classification using Multi Replica with Custom Script

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
export ML_FRAMEWORK=tf-keras
export ML_TASK=img-cls
export TRAIN_TASK=cust-train-multi-replica

```
```
export TUTORIAL_NAME_TRAIN=${ML_FRAMEWORK}-${ML_TASK}-${TRAIN_TASK}

echo "TUTORIAL_NAME: ${TUTORIAL_NAME_TRAIN} for training"
```
```
export TUTORIAL_DIR=${PWD}

echo "TUTORIAL_DIR: ${TUTORIAL_DIR}"
```

### Trainer Task Local Run

```
cd ${TUTORIAL_DIR}
cd trainer && python task.py
rm -rf model
rm -rf logs
```

### Launch a Custom Training Job

##### Configs
###### Single-replica with CPU
```
export CUST_TRAIN_DISPLAY_NAME_SDK=${TUTORIAL_NAME_TRAIN}-sdk-srcpu
export CONTAINER_IMAGE_URI="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-4:latest"

export REPLICA_COUNT=1
export MACHINE_TYPE=n1-standard-4
export ACCELERATOR_COUNT=0
export ACCELERATOR_TYPE=ACCELERATOR_TYPE_UNSPECIFIED
export CONT_ARGS="--replica-count 1"
```

###### Multi-replica with CPU
```
export CUST_TRAIN_DISPLAY_NAME_SDK=${TUTORIAL_NAME_TRAIN}-sdk-mrcpu
export CONTAINER_IMAGE_URI="us-docker.pkg.dev/vertex-ai/training/tf-cpu.2-4:latest"

export REPLICA_COUNT=4
export MACHINE_TYPE=n1-standard-4
export ACCELERATOR_COUNT=0
export ACCELERATOR_TYPE=ACCELERATOR_TYPE_UNSPECIFIED

export CONT_ARGS="--replica-count 4"
```
###### Single-replica with GPU
```
export CUST_TRAIN_DISPLAY_NAME_SDK=${TUTORIAL_NAME_TRAIN}-sdk-srgpu
export CONTAINER_IMAGE_URI="us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-4:latest"

export REPLICA_COUNT=1
export MACHINE_TYPE=n1-standard-4
export ACCELERATOR_COUNT=1
export ACCELERATOR_TYPE=NVIDIA_TESLA_K80

export CONT_ARGS="--replica-count 1"

```
###### Single-replica with GPUs
```
export CUST_TRAIN_DISPLAY_NAME_SDK=${TUTORIAL_NAME_TRAIN}-sdk-srgpus
export CONTAINER_IMAGE_URI="us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-4:latest"

export REPLICA_COUNT=1
export MACHINE_TYPE=n1-standard-32
export ACCELERATOR_COUNT=4
export ACCELERATOR_TYPE=NVIDIA_TESLA_P100

export CONT_ARGS="--replica-count 1"
```
###### Multi-replica with GPUs
```
export CUST_TRAIN_DISPLAY_NAME_SDK=${TUTORIAL_NAME_TRAIN}-sdk-mrgpus
export CONTAINER_IMAGE_URI="us-docker.pkg.dev/vertex-ai/training/tf-gpu.2-4:latest"

export REPLICA_COUNT=2
export MACHINE_TYPE=n1-standard-32
export ACCELERATOR_COUNT=4
export ACCELERATOR_TYPE=NVIDIA_TESLA_P100

export CONT_ARGS="--replica-count 2"

```

##### SDK
```
echo "CUST_TRAIN_DISPLAY_NAME_SDK: ${CUST_TRAIN_DISPLAY_NAME_SDK}"
echo "CONTAINER_IMAGE_URI: ${CONTAINER_IMAGE_URI}"

echo "REPLICA_COUNT: ${REPLICA_COUNT}"
echo "MACHINE_TYPE: ${MACHINE_TYPE}"
echo "ACCELERATOR_COUNT: ${ACCELERATOR_COUNT}"
echo "ACCELERATOR_TYPE: ${ACCELERATOR_TYPE}"

echo "CONT_ARGS: ${CONT_ARGS}"

cd ${TUTORIAL_DIR}
python sdk_custom_training.py \
    --project ${PROJECT} \
    --bucket ${BUCKET} \
    --location ${LOCATION} \
    --display-name ${CUST_TRAIN_DISPLAY_NAME_SDK} \
    --container-image-uri ${CONTAINER_IMAGE_URI} \
    --replica-count ${REPLICA_COUNT} \
    --machine-type ${MACHINE_TYPE} \
    --accelerator-type ${ACCELERATOR_TYPE} \
    --accelerator-count ${ACCELERATOR_COUNT} \
    --container-args ${CONT_ARGS}
```
###### Output Model Artifact
```
gsutil ls gs://${BUCKET}/${CUST_TRAIN_DISPLAY_NAME_SDK}
```

