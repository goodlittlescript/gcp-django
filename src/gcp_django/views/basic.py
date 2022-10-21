from django.http import HttpResponse
from http import HTTPStatus

import logging
logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("GCP Django\n")

def return_status(request, status):
    logger.info(f"Status: {status}")
    response = next((s.phrase for s in HTTPStatus if s == status), status)
    return HttpResponse(f"{response}\n", status=status)

def raise_error(request, message='Boom!'):
    raise Exception(message)
