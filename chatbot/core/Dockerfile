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

# Set environment variables
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 nginx curl && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /opt/program

# Copy installed Python packages and binaries from build stage
COPY --from=build-env /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=build-env /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY --from=build-env /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Copy application code
COPY /src /opt/program/src

# Make scripts executable
RUN chmod +x /opt/program/src/serve_app.py /opt/program/src/start_ollama.sh

# SageMaker entry point
ENTRYPOINT ["python", "/opt/program/src/serve_app.py"]