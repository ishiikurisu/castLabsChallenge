from unittest import TestCase, main
import json

from app import app


# sets the app to testing mode
app.testing = True


class TestProxy(TestCase):
    # Tests for the HTTP server
    def setup(self):
        pass

    def test_can_append_request(self):
        with app.test_client() as client:
            # send data as POST form to endpoint
            sent = {'return_url': 'my_test_url'}
            result = client.post(
                '/',
                data=sent,
            )
            # check result from server with expected data
            self.assertEqual(
                result.data.decode("utf-8"),
                json.dumps(sent)
            )


if __name__ == '__main__':
    main()
