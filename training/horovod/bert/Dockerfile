FROM horovod-wrapper:latest

ARG GCS_OUTPUT_PATH
ARG STAGE_GCS_PATH 
# Set these environment variables to copy input files from GCS.
# ENV STAGE_GCS_PATH ${STAGE_GCS_PATH}
# Set these environment variables to copy output files to GCS.
ENV GCS_OUTPUT_PATH ${GCS_OUTPUT_PATH}

# Alternatively, use NVIDIA's official branch and apply the fix 
# in PR https://github.com/NVIDIA/DeepLearningExamples/pull/386.
RUN git clone --branch bert-fix https://github.com/changlan/DeepLearningExamples.git && \
    pip install git+https://github.com/NVIDIA/dllogger.git

WORKDIR /input

RUN mkdir -p google_pretrained_weights && \
    mkdir -p squad && \
    wget -O squad/train-v1.1.json https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json && \
    cd google_pretrained_weights && \
    wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-24_H-1024_A-16.zip && \
    unzip -o uncased_L-24_H-1024_A-16.zip && \
    rm uncased_L-24_H-1024_A-16.zip

WORKDIR /output

CMD ["python", "/infra/DeepLearningExamples/TensorFlow/LanguageModeling/BERT/run_squad.py", \
     "--noamp", \
     "--vocab_file=/input/google_pretrained_weights/uncased_L-24_H-1024_A-16/vocab.txt", \
     "--bert_config_file=/input/google_pretrained_weights/uncased_L-24_H-1024_A-16/bert_config.json", \
     "--init_checkpoint=/input/google_pretrained_weights/uncased_L-24_H-1024_A-16/bert_model.ckpt", \
     "--train_file=/input/squad/train-v1.1.json", \
     "--learning_rate=2.5e-6", \
     "--output_dir=/output/", \
     "--dllog_path=/output/bert_dllog.json", \
     "--train_batch_size=3", \
     "--num_train_epochs=2", \
     "--max_seq_length=384", \
     "--doc_stride=128", \
     "--do_train", \
     "--horovod"]
