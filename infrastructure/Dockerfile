FROM python:3.9.14-slim-buster

ARG MLFLOW_BUCKET_NAME $MLFLOW_BUCKET_NAME

RUN pip install mlflow

CMD mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://$MLFLOW_BUCKET_NAME/ --host 0.0.0.0 -p 8080
