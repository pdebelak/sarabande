.PHONY: setup test init_db console run_tests print_coverage install_python_dependencies install_js_dependencies install_dependencies

test: run_tests print_coverage

server: venv
	FLASK_APP=simple_site FLASK_ENV=development venv/bin/flask run

webpack:
	yarnpkg run dev

setup: install_dependencies init_db

console: venv
	venv/bin/python

init_db: venv
	venv/bin/python -c "__import__('simple_site').db.create_all()"

run_tests: venv
	venv/bin/coverage run --source simple_site setup.py test

print_coverage: venv
	venv/bin/coverage report -m

install_dependencies: install_python_dependencies install_js_dependencies

install_python_dependencies: venv setup.py
	venv/bin/pip install -e .[dev]

install_js_dependencies: package.json
	yarnpkg

venv:
	python3 -m venv venv && venv/bin/pip install --upgrade pip && venv/bin/pip install --upgrade wheel
