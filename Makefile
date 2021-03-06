.PHONY: setup test update_db console run_tests print_coverage \
	install_python_dependencies install_js_dependencies \
	install_dependencies assets package

test: run_tests print_coverage

server: venv
	FLASK_APP=sarabande FLASK_ENV=development venv/bin/flask run

webpack:
	yarnpkg run dev

setup: install_dependencies update_db

assets: install_js_dependencies
	rm -rf sarabande/static/* && yarnpkg run build

console: venv
	venv/bin/python

package: venv
	venv/bin/python setup.py sdist

update_db: venv
	FLASK_ENV=development venv/bin/sarabande --config $(shell pwd)/example_config.yml update_db

migration: venv
	FLASK_APP=sarabande FLASK_ENV=development venv/bin/flask db migrate

clean:
	rm -rf venv && rm -rf node_modules && rm -f sarabande/sarabande_development.sqlite3

run_tests: venv
	venv/bin/coverage run --source sarabande setup.py test

print_coverage: venv
	venv/bin/coverage report -m

install_dependencies: install_python_dependencies install_js_dependencies

install_python_dependencies: venv setup.py
	venv/bin/pip install -e .[dev]

install_js_dependencies: package.json
	yarnpkg

venv:
	python3 -m venv venv && venv/bin/pip install --upgrade pip && venv/bin/pip install --upgrade wheel
