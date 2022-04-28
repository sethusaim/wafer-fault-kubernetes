FROM python:3.7-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

CMD [ "python3","-W ignore run.py" ]