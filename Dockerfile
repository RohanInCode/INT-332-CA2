# Use the official Python 3.12 slim image as the base
# "slim" means minimal OS packages — keeps the image small
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first so Docker can cache the pip install layer
COPY requirements.txt .

# Install Python packages — no cache keeps image size small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app/ directory into /app inside the container
COPY app/ .

# Create a non-root user named "appuser" for security best practices
RUN adduser --disabled-password --gecos "" appuser

# Switch to the non-root user for all following commands
USER appuser

# Document that the container listens on port 5000
EXPOSE 5000

# Start gunicorn (production WSGI server) bound to 0.0.0.0:5000
# main:app → the Flask "app" object in main.py
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000", "--workers", "2"]
