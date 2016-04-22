#! /bin/bash

gunicorn --config gunicorn.conf runserver:app
