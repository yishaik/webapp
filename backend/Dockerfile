# Use an official Python runtime as a parent image
# python:3.10-slim-bullseye is a good choice for size and compatibility, often available for ARM.
FROM python:3.10-slim-bullseye

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if any were needed (none specified for now)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size
# --user is not used here to keep it simple, but could be for better security if needed.
# Ensure pip is up-to-date
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
# This command will be run when the container starts
# Using "main:app" assuming your FastAPI app instance is named 'app' in 'main.py'
# Running on 0.0.0.0 makes it accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
