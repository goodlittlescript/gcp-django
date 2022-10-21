from django.test import TestCase
import json

class GcpDjangoViewsBasicTests(TestCase):
    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GCP Django")

    def test_echo_get(self):
        response = self.client.get('/echo', {'key': 'value'}, HTTP_X_KEY='Value')
        self.assertJSONEqual(response.content, {
            'url': 'http://testserver/echo?key=value',
            'method': 'GET',
            'headers': {
                'Cookie': '',
                'X-Key': 'Value'
            },
            'body': '',
        })

    def test_echo_put(self):
        response = self.client.put('/echo', 'thebody', HTTP_X_KEY='Value')
        self.assertJSONEqual(response.content, {
            'url': 'http://testserver/echo',
            'method': 'PUT',
            'headers': {
                'Content-Length': '7',
                'Content-Type': 'application/octet-stream',
                'Cookie': '',
                'X-Key': 'Value'
            },
            'body': 'thebody',
        })

    def test_echo_post(self):
        response = self.client.post('/echo', {'key': 'value'}, HTTP_X_KEY='Value')
        self.assertJSONEqual(response.content, {
            'url': 'http://testserver/echo',
            'method': 'POST',
            'headers': {
                'Content-Length': '91',
                'Content-Type': 'multipart/form-data; boundary=BoUnDaRyStRiNg',
                'Cookie': '',
                'X-Key': 'Value'
            },
            'body': 
                '--BoUnDaRyStRiNg\r\n'
                'Content-Disposition: form-data; name="key"\r\n'
                '\r\n'
                'value\r\n'
                '--BoUnDaRyStRiNg--\r\n',
        })

    def test_return_status(self):
        response = self.client.get('/status/200')
        self.assertContains(response, "OK", status_code=200)

        response = self.client.post('/status/404')
        self.assertContains(response, "Not Found", status_code=404)

    def test_raise_error(self):
        with self.assertRaisesRegexp(Exception, 'Boom!') as err:
            self.client.get('/error')
