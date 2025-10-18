# Multi-stage Dockerfile for NeuroDegenerAI
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy shared library
COPY shared/ /app/shared/

# Copy project files
COPY neurodegenerai/ /app/neurodegenerai/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r neurodegenerai/requirements.txt

# Create directories
RUN mkdir -p /app/data /app/models /app/reports /app/assets

# API Stage
FROM base as api

# Set Python path
ENV PYTHONPATH="/app:/app/shared:/app/neurodegenerai/src"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run API
CMD ["python", "-m", "uvicorn", "neurodegenerai.src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]

# UI Stage
FROM base as ui

# Set Python path
ENV PYTHONPATH="/app:/app/shared:/app/neurodegenerai/src"

# Expose port
EXPOSE 8501

# Run Streamlit UI
CMD ["streamlit", "run", "neurodegenerai/src/app/streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
