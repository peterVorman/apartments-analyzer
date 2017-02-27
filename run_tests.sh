#!/usr/bin/env bash

python setup.py test

coverage run --source=analyzer setup.py test