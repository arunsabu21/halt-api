#!/bin/sh
set -e

python manage.py migrate --noinput

python manage.py collectstatic --noinput

celery -A core worker --loglevel=info --concurrency=1 &

exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 1 \
    --access-logfile -