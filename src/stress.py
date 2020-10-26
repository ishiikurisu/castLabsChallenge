from unittest import main, TestCase
import json

from requests import post


class TestStress(TestCase):
    stress_endpoint = "http://192.168.1.118"
    data = [
        {
            "name": "Sponge Bob",
            "job": "Cook",
        }, {
            "name": "Squidward",
            "job": "Artist",
        }, {
            "name": "パトリック",
            "job": "石の下に住む",
        }
    ]


    def test_stress(self):
        for expected_data in self.data:
            result = post(self.stress_endpoint, data=expected_data)

            self.assertEqual(result.status_code, result.status_code)

            result_data = json.loads(result.text)['json']

            self.assertEqual(expected_data['name'], result_data['name'])
            self.assertEqual(expected_data['job'], result_data['job'])
