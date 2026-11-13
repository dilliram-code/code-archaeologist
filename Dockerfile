# Multi-stage Dockerfile for Python-Eel
FROM python:3.11-slim AS base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Eel and dependencies
COPY pyproject.toml setup.py README.md ./
COPY eel/ ./eel/

RUN pip install --no-cache-dir -e .[jinja2]

# Copy examples for verification
COPY examples/ ./examples/

EXPOSE 8000

# Default command: run hello_world example in headless / web server mode
CMD ["python", "examples/01 - hello_world/hello.py"]

