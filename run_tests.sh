#!/usr/bin/env bash


docker-compose up -d dev
docker-compose exec dev bash -c "pip3 install -e ."
docker-compose exec dev bash -c "pip3 install coverage coveralls"
docker-compose exec dev bash -c "coverage run --source=analyzer setup.py test"
docker-compose exec dev bash -c "coveralls"

