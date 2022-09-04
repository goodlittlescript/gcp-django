from django.test import TestCase
import json

class GcpDjangoViewTests(TestCase):
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GCP Django")

    def test_healthcheck(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(response.status_code, 200)
        response_obj = json.loads(response.content)
        self.assertEqual('ok', response_obj['status'])

    def test_boom(self):
        with self.assertRaisesRegexp(Exception, 'Boom!') as err:
            self.client.get('/boom')
