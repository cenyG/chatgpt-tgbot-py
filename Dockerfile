FROM python:3-slim

COPY . /app
RUN pip install -r rq.txt

WORKDIR /app
ENTRYPOINT ["python", "main.py"]