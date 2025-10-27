#!/bin/bash
set -e

cp .env.example .env
docker-compose up -d --build
make migrate
make run
