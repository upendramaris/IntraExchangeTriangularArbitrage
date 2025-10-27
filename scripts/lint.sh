#!/bin/bash
set -e

poetry run black --check .
poetry run ruff check .
