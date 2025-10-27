#!/bin/bash
set -e

poetry run black .
poetry run ruff --fix .
