FROM python:3.7-slim-bullseye

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python","run.py"]