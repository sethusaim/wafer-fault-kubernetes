FROM python:3.9.14-slim-buster

RUN pip install mlflow

CMD mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://wafer-mlflow-35789c9/ --host 0.0.0.0 -p 8000
