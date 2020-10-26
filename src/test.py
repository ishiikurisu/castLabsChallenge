from unittest import TestCase, main
import json
import jwt
from time import time
from datetime import datetime

from requests import post

from app import *


# sets the app to testing mode
app.testing = True


class TestProxy(TestCase):
    # Tests for the HTTP server
    def setup(self):
        pass

    def verify_appendix(self, appendix):
        result = jwt.decode(
            generate_jwt_appendix(),
            SECRET,
            algorithms=['HS512'],
        )

        iat = result['iat']
        jti = result['jti']
        payload = result['payload']

        self.assertEqual(type(iat), int)
        self.assertEqual(type(jti), str)
        self.assertEqual(
            json.dumps(payload),
            json.dumps({
                "user": "username",
                "date": datetime.now().strftime("%Y-%m-%d"),
            }),
        )

    def test_appendix_creation(self):
        appendix = generate_jwt_appendix()
        self.verify_appendix(appendix)

    def test_can_append_request(self):
        # POSTing this URL should return name, job, id, and createdAt
        url = "https://reqres.in/api/users"

        data = {
            "name": "Sponge Bob",
            "job": "Cook",
        }

        expected = post(url, data=data)

        result = proxy_post(url=url, data=data, headers=None)

        self.assertEqual(expected.status_code, result.status_code)
        expected_data = json.loads(expected.text)
        result_data = json.loads(result.data.decode("UTF-8"))
        self.assertEqual(expected_data['name'], result_data['name'])
        self.assertEqual(expected_data['job'], result_data['job'])
        self.assertEqual(data['name'], result_data['name'])
        self.assertEqual(data['job'], result_data['job'])

        self.verify_appendix(result.headers['x-my-jwt'])

    def test_generate_cryptographic_nonces(self):
        previous_nonces = set()
        for _ in range(10000):
            new_nonce = generate_cryptographic_nonce()
            self.assertTrue(new_nonce not in previous_nonces)
            previous_nonces.add(new_nonce)

    def test_status_page(self):
        with app.test_client() as client:
            response = client.get('/status')
            status = json.loads(response.data.decode('utf-8'))
            checkpoint = status['from_start']

            for i in range(0, 500):
                response = client.get('/status')
                status = json.loads(response.data.decode('utf-8'))
                from_start = status['from_start']
                self.assertTrue(from_start > checkpoint)
                checkpoint = from_start


if __name__ == '__main__':
    main()
