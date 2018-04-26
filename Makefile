.PHONY: setup test init_db

test: venv
	venv/bin/python setup.py test

start: venv
	FLASK_APP=simple_site venv/bin/flask run

setup: install_dependencies init_db

install_dependencies: venv setup.py
	venv/bin/pip install -e .[dev]

init_db: venv
	venv/bin/python -c "__import__('simple_site').db.create_all()"

console: venv
	venv/bin/python

venv:
	python3 -m venv venv && venv/bin/pip install --upgrade pip && venv/bin/pip install --upgrade wheel
