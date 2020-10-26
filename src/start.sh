#!/bin/bash

set -x

export FLASK_APP=app.py
export FLASK_RUN_HOST=0.0.0.0
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

python3 -m pip install -r requirements.txt
python3 -m flask run
