SHELL := /bin/bash

.PHONY: run format lint test

run:
	poetry run python -m triarb.main



format:
	poetry run black .
	poetry run ruff --fix .

lint:
	poetry run black --check .
	poetry run ruff check .

test:
	poetry run pytest
