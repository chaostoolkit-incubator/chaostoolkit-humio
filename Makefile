.PHONY: install
install:
	pip install --upgrade pip setuptools wheel
	pip install .

.PHONY: install-dev
install-dev: install
	pip install .[dev]
	pip install .

.PHONY: build
build:
	python -m build

.PHONY: lint
lint:
	ruff chaoshumio/ tests/
	isort --check-only --line-length 80 --profile black chaoshumio/ tests/
	black --check --diff --line-length=80 chaoshumio/ tests/
	mypy chaoshumio/ tests/

.PHONY: format
format:
	isort --line-length 80 --profile black chaoshumio/ tests/
	black --line-length=80 chaoshumio/ tests/
	ruff --fix chaoshumio/ tests/

.PHONY: tests
tests:
	pytest
