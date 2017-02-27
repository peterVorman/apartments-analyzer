#!/usr/bin/env bash
cd tests
pip install -r requirements.txt
pytest -v --color=yes --flake8 ./

cd ../
coverage run --source=analyzer