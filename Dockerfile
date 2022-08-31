FROM python:3.10-slim

# Setup appuser and app dir
RUN groupadd -g 1001 appuser && \
    useradd -r -u 1001 -g appuser appuser -m -s /bin/bash && \
    mkdir -p /app && \
    chown appuser:appuser /app
WORKDIR /app

# Install development dependencies
RUN apt-get update && \
    apt-get install -y curl jq && \
    rm -rf /var/lib/apt/lists/*

# Install project dependencies
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

USER appuser

COPY --chown appuser:appuser . /app
CMD ["/app/bin/run"]
