import json
from time import time
from datetime import datetime
from random import randint

from flask import (
    Flask,
    request,
)
import jwt
from requests import post


SECRETS = dict()
SECRET = "TODO LOAD SECRET"
UPSTREAM = "https://reqres.in/api/users"
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


@app.route('/', methods=['POST'])
def index():
    # generating response
    response = post(UPSTREAM, data=request.data, headers=request.headers)

    # appending header to response
    response.headers['x-my-jwt'] = generate_jwt_appendix()

    return (
        response.content,
        response.status_code,
        response.headers.items(),
    )


if __name__ == '__main__':
    app.run()
