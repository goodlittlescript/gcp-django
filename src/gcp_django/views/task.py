from django.http import HttpResponse
from google.cloud import tasks_v2
import json
import os
import datetime

import logging
logger = logging.getLogger(__name__)

object_name = 'last-data'
service_account_email = os.environ['CLOUDTASKS_SERVICE_ACCOUNT_EMAIL']
queue = os.environ['CLOUDTASKS_QUEUE']
audience = os.environ['CLOUDRUN_AUDIENCE']

def run(request):
    logger.info(f"Ran task")
    return HttpResponse('Ok')

def enqueue(request):
    logger.info(f"Enqueue task")
    if queue == "local":
        return run(request)

    client = tasks_v2.CloudTasksClient()
    task = {
        'http_method': 'POST',
        'url'        : f'https://${audience}/schedule/run',
        'headers': {
            'traceparent': request.headers.get('traceparent', ''),
        },
        'oidc_token': {
            'service_account_email': service_account_email,
            'audience': audience,
        },
    }
    response = client.create_task(request={
        "parent": parent,
        "task": task
    })
    return HttpResponse(response)

