FROM python:3-slim

COPY . /app
WORKDIR /app

RUN pip install -r rq.txt

ENTRYPOINT ["python", "main.py"]