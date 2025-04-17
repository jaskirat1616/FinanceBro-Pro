FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    FLASK_ENV=production \
    FLASK_APP=run.py

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libc6-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the app
RUN addgroup --system app && adduser --system --group app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir lxml[html_clean]>=4.9.3 && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m nltk.downloader punkt

# Copy the rest of the application
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/instance && \
    chown -R app:app /app

# Switch to non-root user
USER app

# Expose the port
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--worker-class", "gevent", "--config", "gunicorn_config.py", "run:app"] 