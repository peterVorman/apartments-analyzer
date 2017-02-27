#!/usr/bin/env bash
pip install -r ./tests/requirements.txt
pytest -v --color=yes --flake8 ./tests/
coverage run --source=analyzer tests