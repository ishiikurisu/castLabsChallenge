import json
from time import time
from datetime import datetime

from flask import (
    Flask,
    request,
    Response,
)
import jwt


SECRETS = dict()
SECRET = "TODO LOAD SECRET"
with open("./config/secrets.json") as fp:
    SECRETS = json.loads(fp.read())
    SECRET = SECRETS.get('JWT_SECRET', 'FAILED TO LOAD SECRET')
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
            "date": datetime.now().strftime("%Y-%m-%d"),
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
