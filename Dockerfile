# Use an official Python runtime as a base image
FROM python:3.9-slim
ARG USER=1001
ARG PORT=80

# Set environment variables to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE ${PORT}

USER $USER

HEALTHCHECK --interval=60s CMD curl -f http://localhost:${PORT}/ping || exit 1

# Command to run the Flask app
CMD ["python", "app.py"]
