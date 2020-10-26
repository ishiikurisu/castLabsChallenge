FLASK_APP=app.py

default: build run

build:
	pip install -r requirements.txt

run:
	flask run

test:
	python -m unittest test.py

stress:
	python -m unittest  stress.py
