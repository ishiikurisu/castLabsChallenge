import json
from time import time
from datetime import datetime
from random import randint

from flask import (
    jsonify,
    Flask,
    request,
    Response,
)
import jwt
from requests import post


SECRETS = dict()
SECRET = "TODO LOAD SECRET"
UPSTREAM = "TODO LOAD UPSTREAM"
FROM_START = time()
PROCESSED_REQUESTS = 0
with open("./config/secrets.json") as fp:
    SECRETS = json.loads(fp.read())
    SECRET = SECRETS.get('JWT_SECRET', 'FAILED TO LOAD SECRET')
    UPSTREAM = SECRETS.get('UPSTREAM', UPSTREAM)
app = Flask(__name__)


def generate_cryptographic_nonce(length=17):
    # this function's strategy was extracted from `python-oauth2`
    return ''.join([str(randint(0, 9)) for i in range(length)])


def generate_jwt_appendix():
    appendix = {
        'iat': int(time()),
        'jti': generate_cryptographic_nonce(),
        'payload': {
            "user": "username",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
    }
    return jwt.encode(appendix, SECRET, algorithm='HS512')


def proxy_post(url, data, headers):
    # generating response
    response = post(url, data=data, headers=headers)

    # appending header to response
    response.headers['x-my-jwt'] = generate_jwt_appendix()

    return Response(
        response=response.content,
        status=response.status_code,
        headers=response.headers.items(),
    )


def increment_processed_requests(f):
    def inner():
        PROCESSED_REQUESTS += 1
        return f
    return inner


@increment_processed_requests
@app.route('/', methods=['POST'])
def index():
    return proxy_post(
        url=UPSTREAM,
        data=request.data,
        headers=request.headers,
    )


@increment_processed_requests
@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "from_start": time() - FROM_START,
        "processed_requests": PROCESSED_REQUESTS,
    })


if __name__ == '__main__':
    app.run()