from django.http import HttpResponse
import json

import logging
logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("GCP Django")

def healthcheck(request):
    logger.info("Performing healthcheck")
    response = {'status': 'ok'}
    return HttpResponse(json.dumps(response))

def boom(request):
    raise Exception('Boom!')
