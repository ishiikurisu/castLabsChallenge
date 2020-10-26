from unittest import TestCase, main
import json
import jwt
from time import time
from datetime import datetime

from app import app, SECRET


# sets the app to testing mode
app.testing = True


class TestProxy(TestCase):
    # Tests for the HTTP server
    def setup(self):
        pass

    def test_can_append_request(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            expected = {'return_url': 'my_test_url'}
            raw_result = client.post('/', data=expected)
            result = json.loads(raw_result.data.decode("utf-8"))

            # checking if appended JWT is correct
            appendix = jwt.decode(
                result['x-my-jwt'],
                SECRET,
                algorithms=['HS512'],
            )
            iat = appendix['iat']
            jti = appendix['jti']
            payload = appendix['payload']
            self.assertEqual(
                type(iat),
                int,
            )
            self.assertEqual(
                type(jti),
                int,
            )
            self.assertEqual(
                json.dumps(payload),
                json.dumps({
                    "user": "username",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                }),
            )

            # checking if remaining payload is intact
            del result['x-my-jwt']
            self.assertEqual(
                json.dumps(result),
                json.dumps(expected),
            )


if __name__ == '__main__':
    main()
