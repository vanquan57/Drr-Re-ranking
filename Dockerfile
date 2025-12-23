# Use Python 3.7 with Ubuntu 18.04 for TensorFlow 1.x compatibility
FROM python:3.7-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create log directory
RUN mkdir -p /app/log

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command - keep container running
CMD ["tail", "-f", "/dev/null"]

