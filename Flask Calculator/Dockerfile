# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# create data dir
RUN mkdir -p /data/histories
VOLUME ["/data"]

EXPOSE 5000
ENV FLASK_RUN_PORT=5000

CMD ["python", "app.py"]
