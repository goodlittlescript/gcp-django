FROM --platform=linux/amd64 python:3.10-slim

# Setup appuser and app dir
RUN groupadd -g 1001 appuser && \
    useradd -r -u 1001 -g appuser appuser -m -s /bin/bash && \
    mkdir -p /app && \
    chown appuser:appuser /app
WORKDIR /app

# Install platform dependencies
ARG BERGLAS_VERSION=1.0.1
RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y curl && \
    curl -OL "https://github.com/GoogleCloudPlatform/berglas/releases/download/v${BERGLAS_VERSION}/berglas_${BERGLAS_VERSION}_linux_amd64.tar.gz" && \
    tar xvzf "berglas_${BERGLAS_VERSION}_linux_amd64.tar.gz" && \
    mv berglas /bin/berglas && \
    rm /app/* && \
    apt-get remove -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install project dependencies
ENV PATH=/home/appuser/.local/bin:$PATH
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# Install development dependencies
RUN apt-get update && \
    apt-get install -y procps curl jq && \
    curl -o /usr/local/bin/ts -L https://raw.githubusercontent.com/thinkerbot/ts/master/bin/ts && \
    chmod +x /usr/local/bin/ts

USER appuser

COPY --chown=appuser:appuser . /app
CMD ["/bin/berglas", "exec", "/app/bin/run"]
