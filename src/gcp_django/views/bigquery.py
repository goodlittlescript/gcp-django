from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from google.cloud import bigquery
import json
import os
from datetime import datetime
from uuid import uuid4

import logging
logger = logging.getLogger(__name__)

bigquery_project = os.environ['BIGQUERY_PROJECT']


@method_decorator([csrf_exempt], name='dispatch')
class BigqueryApi(View):
    def get_response(self, request):
        now = datetime.now().astimezone()
        data = request.body.decode('utf-8') or "null"
        record = {
            "table": "gcp_django.requests",
            "extracted_at": now.replace(microsecond=0).isoformat(),
            "metadata": {
                "userAgent": request.headers["User-Agent"]
            },
            "data": json.loads(data),
        }
        response = {"records": [record]}
        return response

    def get(self, request):
        response = self.get_response(request)
        return JsonResponse(response)

    def post(self, request):
        response = self.get_response(request)
        records = response["records"]

        rows_by_table = {}
        for record in records:
            record["uuid"] = uuid4()
            table = record["table"]
            row = {
                "uuid": str(record["uuid"]),
                "extracted_at": record["extracted_at"],
                "metadata": json.dumps(record["metadata"]),
                "data": json.dumps(record["data"]),
            }
            if table in rows_by_table:
                rows_by_table[table].append(row)
            else:
                rows_by_table[table] = [row]

        errors = []
        client = bigquery.Client(project=bigquery_project)
        for table, rows in rows_by_table.items():
            errors += client.insert_rows_json(table, rows)

        response["errors"] = errors
        return JsonResponse(response)
