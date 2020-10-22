FLASK_APP=app.py

default: build run

build:
	pip install -r requirements.txt

run:
	flask run
