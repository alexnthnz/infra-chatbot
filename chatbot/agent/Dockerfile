# Stage 1: Build environment
FROM python:3.13-slim AS build-env

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf ~/.cache/pip && \
    find /usr/local/lib/python3.13/site-packages -name "*.pyc" -delete && \
    find /usr/local/lib/python3.13/site-packages -name "__pycache__" -exec rm -r {} +

# Stage 2: Final image
FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=build-env /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build-env /usr/local/bin/uvicorn /usr/local/bin/uvicorn

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
