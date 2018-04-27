.PHONY: setup test init_db console run_tests print_coverage

test: run_tests print_coverage

start: venv
	FLASK_APP=simple_site venv/bin/flask run

setup: install_dependencies init_db

console: venv
	venv/bin/python

init_db: venv
	venv/bin/python -c "__import__('simple_site').db.create_all()"

run_tests: venv
	venv/bin/coverage run --source simple_site setup.py test

print_coverage: venv
	venv/bin/coverage report -m

install_dependencies: venv setup.py
	venv/bin/pip install -e .[dev]

venv:
	python3 -m venv venv && venv/bin/pip install --upgrade pip && venv/bin/pip install --upgrade wheel
