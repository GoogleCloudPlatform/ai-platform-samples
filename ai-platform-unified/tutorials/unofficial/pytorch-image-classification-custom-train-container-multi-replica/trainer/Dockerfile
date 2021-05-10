FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime

COPY . /trainer

WORKDIR /trainer

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "task"]