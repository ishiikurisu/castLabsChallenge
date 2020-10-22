import json
from time import time

from flask import (
    Flask,
    request,
    Response,
)
import jwt


SECRET = 'TODO load secret'
app = Flask(__name__)


def generate_cryptographic_nonce():
    # TODO improve crpytographic nonce
    return 123


@app.route('/', methods=['POST'])
def index():
    # creating appendix
    appendix = {
        'iat': int(time()),
        'jti': generate_cryptographic_nonce(),
        'payload': {
            "user": "username",
            "date": "todays date",
        },
    }
    my_jwt = jwt.encode(appendix, SECRET, algorithm='HS512')

    # appending JWT to POST request
    form = dict(request.form)
    form['x-my-jwt'] = my_jwt.decode('utf-8')

    # generating response
    return Response(
        response=json.dumps(form),
        mimetype='application/json',
    )


if __name__ == '__main__':
   app.run()
