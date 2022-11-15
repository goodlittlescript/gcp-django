bind = "0.0.0.0:8080"
workers = 1
threads = 8
timeout = 0

import os
import google.cloud.logging
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'plaintext': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S %z',
        },
    },
    'filters': {},
    'handlers': {
        'console': {
            'class': 'google.cloud.logging.handlers.StructuredLogHandler',
            'project_id': google.cloud.logging.Client().project,
        } if os.environ.get('DJANGO_LOG_FORMAT', 'json') == 'json' else {
            'class': 'logging.StreamHandler',
            'formatter': 'plaintext',
        }
    },
    'loggers': {
        'gunicorn.access': {
            'handlers': ['console'],
            'level': os.environ.get('GUNICORN_ACCESS_LOG_LEVEL', 'WARN'),
        },
        'gunicorn.error': {
            'handlers': ['console'],
            'level': os.environ.get('GUNICORN_ERROR_LOG_LEVEL', 'INFO'),
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.environ.get('DJANGO_LOG_LEVEL', 'WARN'),
    },
}
