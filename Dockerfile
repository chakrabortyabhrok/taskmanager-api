#The Comments are for understanding purposes, If needed later.

# Base Image: Light Weight Python env
FROM python:3.12-slim

# Environment Variables:
# - PYTHONUNBUFFERED: Keeps Python from buffering stdout/stderr (vital for container logs)
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Working Directory inside the container
WORKDIR /app

# Install System Dependencies
# libpq-dev and gcc are needed if you are using PostgreSQL (psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Dependency Layer Caching
# Copy dependency file FIRST so Docker caches this layer unless requirements change
COPY requirements.txt /app/

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the application code
COPY . /app/

# Collect Static Files (Optional for production)
# RUN python manage.py collectstatic --noinput

# Expose the port to Gunicorn
EXPOSE 8000

# Default Command: Start the app with Gunicorn
# Replace 'taskmanager_api.wsgi:application' with 'YOUR_PROJECT_NAME.wsgi:application'
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "taskmanager_api.wsgi:application"]

