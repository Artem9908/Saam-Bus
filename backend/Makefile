.PHONY: clean test coverage lint format install dev-install

clean:
	./scripts/cleanup.sh

test:
	pytest

coverage:
	pytest --cov=app --cov-report=term-missing

lint:
	flake8 app tests
	mypy app tests

format:
	black app tests
	isort app tests

install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt -r requirements-dev.txt