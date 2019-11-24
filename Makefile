.PHONY: build

MODULE:=mydevoirs

all: dev test

install:
	python3.7 -m venv .venv
	.venv/bin/pip install -U pip	
	poetry install

devtools:
	.venv/bin/pip install -U ipython pdbpp autoflake

dev:  install devtools 

test:
	poetry run pytest

cov:
	rm -rf .pytest_cache
	poetry run coverage run -m pytest
	poetry run coverage report

cov_html: cov
	poetry run coverage html
	firefox htmlcov/index.html &
	
pdb:
	poetry run pytest --pdb


run:
	poetry run python main.py

isort:
	poetry run isort main.py
	poetry run isort -rc mydevoirs
	poetry run isort -rc tests

black:
	poetry run black mydevoirs tests main.py

style: isort black

remove_unused_imports: isort
	poetry run autoflake -r -i --remove-all-unused-imports mydevoirs tests 



clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-full: clean clean-venv

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name 'requirements*' -exec rm -f {} +
	rm -rf docs/_build/



clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -rf .pytest_cache/

clean-venv:
	rm -rf .venv/

ipython:
	.venv/bin/ipython

build:
	poetry run scripted/build_executable.py