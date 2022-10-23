from django.http import HttpResponse
from google import auth
from google.cloud import storage
import json
import os
import datetime

import logging
logger = logging.getLogger(__name__)

object_name = 'last-data'
bucket_name = os.environ['DATA_BUCKET']


def get_data(request):
    logger.info(f"Get data: {object_name}")
    bucket = storage.Client(project).get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    response = blob.download_as_string()
    return HttpResponse(response)


def set_data(request):
    logger.info(f"Set data: {object_name}")
    bucket = storage.Client(project).get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    now = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc, microsecond=0)
    data = {"lastUpdate": now.isoformat().replace('+00:00', 'Z')}
    data_str = json.dumps(data)
    blob.upload_from_string(data_str)
    return HttpResponse(data_str)




def get_data_url(request):
    logger.info(f"Get url: {object_name}")
    bucket = storage.Client(project).get_bucket(bucket_name)
    blob = bucket.blob(object_name)
    credentials, project = auth.default()
    credentials.refresh(auth.transport.requests.Request())
    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="GET",
        service_account_email='rt-gcp-django@goodlittlescript-io-dev.iam.gserviceaccount.com',
        access_token=credentials.token
    )
    return HttpResponse(url)