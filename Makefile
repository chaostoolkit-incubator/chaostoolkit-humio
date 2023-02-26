.PHONY: install
install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

.PHONY: install-dev
install-dev: install
	pip install -r requirements-dev.txt
	python setup.py develop

.PHONY: build
build:
	python setup.py build

.PHONY: lint
lint:
	flake8 chaoshumio/ tests/
	isort --check-only --profile black chaoshumio/ tests/
	black --check --diff --line-length=80 chaoshumio/ tests/
	mypy chaoshumio/ tests/

.PHONY: format
format:
	isort --profile black chaoshumio/ tests/
	black --line-length=80 chaoshumio/ tests/

.PHONY: tests
tests:
	pytest
