from django.http import HttpResponse
from google.cloud import tasks_v2
import os
import json

import logging
logger = logging.getLogger(__name__)

service_url = os.environ['CLOUDRUN_SERVICE_URL']
service_account_email = os.environ['CLOUDTASKS_SERVICE_ACCOUNT_EMAIL']
queue = os.environ['CLOUDTASKS_QUEUE']


def run(request):
    logger.info(f"Ran task")
    return HttpResponse('Ok')


def enqueue(request):
    logger.info(f"Enqueue task")
    if queue == "local":
        return run(request)

    client = tasks_v2.CloudTasksClient()
    task = {
        'http_request': {
            'http_method': tasks_v2.HttpMethod.GET,
            'url': f'{service_url}/task/run',
            'headers': {
                'traceparent': request.headers.get('traceparent', ''),
            },
            'oidc_token': {
                'service_account_email': service_account_email,
                'audience': service_url,
            },
        },
    }
    response = client.create_task(request={"parent": queue, "task": task})
    return HttpResponse(
        f'Created: {response.create_time} ({response.http_request.url})')
