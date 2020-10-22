import json

from flask import Flask, request, Response


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    form = dict(request.form)

    return Response(
      response=json.dumps(form),
      mimetype='application/json',
   )


if __name__ == '__main__':
   app.run()
