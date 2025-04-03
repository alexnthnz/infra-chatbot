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

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 nginx && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/program

COPY --from=build-env /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build-env /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=build-env /usr/local/bin/gunicorn /usr/local/bin/gunicorn

COPY /src /opt/program/src

RUN chmod +x /opt/program/src/serve_app.py

# SageMaker entry point
ENTRYPOINT ["python", "/opt/program/src/serve_app.py"]
