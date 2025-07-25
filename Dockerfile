FROM python:3.10-slim-bookworm

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y awscli && \
    pip install --no-cache-dir -r requirements.txt python-multipart && \
    rm -rf /var/lib/apt/lists/*

CMD ["python3", "app.py"]
