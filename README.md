# castLabs Python Programming Challenge

This is my take on the [castLabs programming task](https://github.com/castlabs/python_programming_task).

This repo implements a [RFC2616](https://www.ietf.org/rfc/rfc2616.txt) proxy
that appends a new field to the request as specified in the task.

## Develop

It's recommended to use virtualenv to execute the app locally. On Unix systems:

``` sh
python3 -m virtualenv venv -p python3
source venv/bin/activate
```

To install requirements:

``` sh
pip install -r requirements.txt
```

To execute the program locally:

``` sh
export FLASK_APP=app.py
flask run
```
