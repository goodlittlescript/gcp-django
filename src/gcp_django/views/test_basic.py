from django.test import TestCase
import json

class GcpDjangoViewsBasicTests(TestCase):
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GCP Django")

    def test_return_status(self):
        response = self.client.get('/status/200')
        self.assertContains(response, "OK", status_code=200)

        response = self.client.post('/status/404')
        self.assertContains(response, "Not Found", status_code=404)

    def test_raise_error(self):
        with self.assertRaisesRegexp(Exception, 'Boom!') as err:
            self.client.get('/error')
