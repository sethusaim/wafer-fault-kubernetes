FROM python:3.7-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python","run.py"]