from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from google.cloud import tasks_v2
import os
import json

import logging
logger = logging.getLogger(__name__)

service_url = os.environ['CLOUDRUN_SERVICE_URL']
service_account_email = os.environ['CLOUDTASKS_SERVICE_ACCOUNT_EMAIL']
queue = os.environ['CLOUDTASKS_QUEUE']


@method_decorator([csrf_exempt], name='dispatch')
class TaskApi(View):
    def get(self, request):
        logger.info(f"Ran task")
        return JsonResponse({'status': 'complete'})

    def post(self, request):
        logger.info(f"Enqueue task")
        if queue == "local":
            return run(request)

        client = tasks_v2.CloudTasksClient()
        task = {
            'http_request': {
                'http_method': tasks_v2.HttpMethod.GET,
                'url': f'{service_url}/task',
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
        return JsonResponse({
            'status': 'created',
            'created_at': 'response.create_time',
            'url': response.http_request.url
        })
