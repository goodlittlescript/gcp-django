from django.http import HttpResponse, JsonResponse
from http import HTTPStatus
import json

import logging
logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("GCP Django\n")


def echo(request):
    response = {
        "url": request.build_absolute_uri(),
        "method": request.META['REQUEST_METHOD'],
        "headers": dict(request.headers),
        "body": request.body.decode('utf-8'),
    }
    return JsonResponse(response, json_dumps_params={'indent': 2})


def return_status(request, status):
    response = next((s.phrase for s in HTTPStatus if s == status), status)
    return HttpResponse(f"{response}\n", status=status)


def raise_error(request, message='Boom!'):
    logger.debug(f"raise_error: {request.META['REQUEST_METHOD']} {request.build_absolute_uri()}")
    logger.info(f"Error Requested: {message}")
    logger.warning(f"Error Pending: {message}")
    logger.error(f"Error Happening: {message}")
    raise Exception(message)
