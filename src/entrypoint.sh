#!/bin/bash
set -e
python -m pip install --upgrade pip
python -m pip install -e .
python -m flask --app flaskapp db upgrade --directory flaskapp/migrations
python -m gunicorn flaskapp