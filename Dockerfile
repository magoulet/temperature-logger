FROM python:3.11-slim

ENV TZ=America/Los_Angeles

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev \
    gcc \
    i2c-tools \
    libgpiod2 \
    curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "run_loop.sh"]
