#!/bin/sh
set -e

python manage.py collectstatic --noinput

exec gunicorn core.wsgi:appication --bind 0.0.0.0:${PORT:-8000} --workers 3