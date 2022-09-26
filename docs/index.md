# GCP Django

An example of typical gcp services, used by django.

## Scope

- Authentication - IAP, Workload Identity Federation
- Serverless Containers - Cloud Run
- Secrets - Google Secret Manager
- SQL Database - CloudSQL
- Static assets - Load Balancer + Storage Bucket
- Cache - Memory Store
- Queue - Cloud Tasks
- Schedule - Cloud Schedule
- Signed URLs
- Monitoring - Cloud Logging
- Errors - Error Reporting

## Routes

- gcp-django.goodlittlescript.io/docs: static assets - mkdocs

## Secrets

- DJANGO_SECRET_KEY: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
