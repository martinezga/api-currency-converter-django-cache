#!/bin/bash

cd /home/appuser/api

python manage.py migrate

exec "$@"
