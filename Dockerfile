FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    g++ \
    cmake \
    python3-pip \
    && pip3 install --no-cache-dir notebook \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /rushhour
COPY . .