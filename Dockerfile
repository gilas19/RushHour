FROM debian:latest

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y \
    g++ \
    cmake \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /rushhour
COPY . .