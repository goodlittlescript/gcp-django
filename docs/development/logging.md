# Logging

The GCP Django app uses the google-cloud-logging package to add structured logging.

_The middleware used in this setup only works for wsgi apps. An asgi app will raise errors. See the [Add support for asgi django apps](https://github.com/googleapis/python-logging/issues/607) issue for more._

## Setup

The logging config is specified in the `gunicorn.conf.py` such that both gunicorn and django (loaded by gunicorn) can be configured in one place. `RequestMiddleware` is added such that google-cloud-logging adds request metadata to the logs including, importantly, trace information.

```python
MIDDLEWARE = [ # ...
    'google.cloud.logging_v2.handlers.middleware.request.RequestMiddleware',
]
```

## Usage

ENV Variables:

- **DJANGO_LOG_FORMAT**: Set to "json" to enable structured logging. Defaults to "json".
- **DJANGO_LOG_LEVEL**: The log level for django loggers. Defaults to "INFO".
- **GUNICORN_ACCESS_LOG_LEVEL**: Defaults to "WARN" (meaning no access logs). Cloudrun produces access logs automatically, thus this default prevents duplicates and is incidentally in line with the [gunicorn default setting](https://docs.gunicorn.org/en/stable/settings.html#logging).
- **GUNICORN_ERROR_LOG_LEVEL**: Defaults to "INFO".

For local development DJANGO_LOG_FORMAT is set to "plaintext", which results in plaintext logs (much more readable). To preview structured logs `unset DJANGO_LOG_FORMAT`.

## Troubleshooting

When previewing structured logs locally by unsetting DJANGO_LOG_FORMAT you may need to set GCLOUD_PROJECT so that the following error does not result:

```
OSError: Project was not passed and could not be determined from the environment.
```

The GCLOUD_PROJECT value will be incorporated into the logs but as the logs are not sent anywhere, the specific value does not matter.
