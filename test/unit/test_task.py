from django.test import TestCase
import json


class TaskApiTests(TestCase):
    def test_tasks(self):
        response = self.client.get('/task')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'complete'})
