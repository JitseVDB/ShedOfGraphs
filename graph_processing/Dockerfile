# Use the official Ubuntu 24.04 image as the base image
FROM ubuntu:24.04

# Set environment variables to disable interactive prompts and to optimize Python behavior
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for the application
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    build-essential \
    gcc \
    make \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Make python3.12 the default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# Install Python packages from the requirements file
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy the entire project to the container
COPY . .

# Build and install the nauty tool
RUN cd nauty2_8_9 && \
    ./configure && \
    make && \
    cp geng /usr/local/bin && \
    cd .. && \
    rm -rf nauty2_8_9

# Expose port 5000 for Flask web server
EXPOSE 5000

# Command to run the Flask web server
CMD ["python", "web_server.py"]
