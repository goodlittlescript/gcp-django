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

## Development

Setup auth:

```shell
gcloud auth login
gcloud auth configure-docker
gcloud auth application-default login
```
