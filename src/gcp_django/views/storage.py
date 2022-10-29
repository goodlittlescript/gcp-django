from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from google.cloud import storage
import json
import os
import datetime

import logging
logger = logging.getLogger(__name__)

object_name = 'last-data'
bucket_name = os.environ['DATA_BUCKET']


@method_decorator([csrf_exempt], name='dispatch')
class StorageApi(View):
    def get(self, request):
        logger.info(f"Get data: {object_name}")
        bucket = storage.Client("").get_bucket(bucket_name)
        blob = bucket.blob(object_name)
        response = blob.download_as_string()
        return HttpResponse(response)

    def post(self, request):
        logger.info(f"Set data: {object_name}")
        bucket = storage.Client("").get_bucket(bucket_name)
        blob = bucket.blob(object_name)
        now = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc, microsecond=0)
        data = {"lastUpdate": now.isoformat().replace('+00:00', 'Z')}
        data_str = json.dumps(data)
        blob.upload_from_string(data_str)
        return HttpResponse(data_str)
