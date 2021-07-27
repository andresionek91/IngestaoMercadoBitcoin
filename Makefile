clean:
	rm -rf .venv day-summary *.checkpoint .pytest_cache .coverage

init: clean
	pip install poetry
	poetry install
	pre-commit install

test:
	poetry run python -m pytest


## CI/CD
ci-test:
	poetry run python -m pytest


