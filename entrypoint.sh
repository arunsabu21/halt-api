#!/bin/sh
set -e

python manage.py migrate --noinput

python manage.py collectstatic --noinput

celery -A core worker --loglevel=info &

exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 3 \
    --access-logfile -