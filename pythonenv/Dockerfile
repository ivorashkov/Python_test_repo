# Use official Python base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose ports for Flask and Prometheus
EXPOSE 8000 8001

# Command to run the application
CMD ["python", "cpu_usage_prometheus_app.py"]
