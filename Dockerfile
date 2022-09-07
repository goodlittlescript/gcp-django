FROM --platform=linux/amd64 python:3.10-slim

# Setup appuser and app dir
RUN groupadd -g 1001 appuser && \
    useradd -r -u 1001 -g appuser appuser -m -s /bin/bash && \
    mkdir -p /app && \
    chown appuser:appuser /app
WORKDIR /app

# Install development dependencies
ARG BERGLAS_VERSION=1.0.1
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y curl jq && \
    curl -OL "https://github.com/GoogleCloudPlatform/berglas/releases/download/v${BERGLAS_VERSION}/berglas_${BERGLAS_VERSION}_linux_amd64.tar.gz" && \
    tar xvzf "berglas_${BERGLAS_VERSION}_linux_amd64.tar.gz" && \
    mv berglas /bin/berglas && \
    rm /app/* && \
    rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

USER appuser

COPY --chown=appuser:appuser bin src /app/
CMD ["/bin/berglas", "exec", "/app/bin/run"]
