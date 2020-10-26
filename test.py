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
        data = {
            "name": "Sponge Bob",
            "job": "Cook",
        }

        # making test request
        expected = post(UPSTREAM, data=data)

        with app.test_client() as client:
            # send data as POST form to endpoint
            result = client.post('/', data=data)

            # TODO verify response to see if they are the same

            # verifying header
            self.verify_appendix(result.headers['x-my-jwt'])

    def test_generate_cryptographic_nonces(self):
        previous_nonce = None
        for _ in range(10000):
            new_nonce = generate_cryptographic_nonce()
            self.assertNotEqual(previous_nonce, new_nonce)
            previous_nonce = new_nonce


if __name__ == '__main__':
    main()
