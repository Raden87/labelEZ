# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for images and labels
RUN mkdir -p images labels

# Create a non-root user with flexible UID/GID
RUN groupadd -r -g 1000 appuser && useradd -r -u 1000 -g appuser appuser

# Set proper permissions
RUN chmod -R 755 /app
RUN chmod +x /app/start.sh
RUN chown -R appuser:appuser /app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Switch to non-root user
USER appuser

# Set the default command
CMD ["/app/start.sh"]

