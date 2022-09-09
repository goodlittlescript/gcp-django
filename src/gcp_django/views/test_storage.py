from django.test import TestCase
import json

class GcpDjangoViewsStorageTests(TestCase):
    def test_get_set(self):
        get_response = self.client.get('/storage/get')
        self.assertEqual(get_response.status_code, 200)

        set_response = self.client.get('/storage/set')
        self.assertEqual(set_response.status_code, 200)

        # demonstrate the data has been updated by confirming the previous
        # lastUpdate timestamp is earlier than current
        get_data = json.loads(get_response.content)
        set_data = json.loads(set_response.content)
        self.assertTrue(set_data['lastUpdate'] > get_data['lastUpdate'])

        get_response = self.client.get('/storage/get')
        self.assertEqual(get_response.status_code, 200)

        # demonstrate that after update the lastUpdate timestamp matches
        # that of the last set response
        get_data = json.loads(get_response.content)
        set_data = json.loads(set_response.content)
        self.assertEqual(set_data['lastUpdate'], get_data['lastUpdate'])
