FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
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

# Install Python packages
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy the entire project
COPY . .

# Build nauty
RUN cd nauty2_8_9 && \
    ./configure && \
    make && \
    cp geng /usr/local/bin && \
    cd .. && \
    rm -rf nauty2_8_9

# Expose Flask default port
EXPOSE 5000

# Start the web server
CMD ["python", "web_server.py"]
