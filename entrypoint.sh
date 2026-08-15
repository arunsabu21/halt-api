#!/bin/sh
set -e

python manage.py migrate --noinput

python manage.py collectstatic --noinput

celery -A core worker --loglevel=info --concurrency=1 &

exec supervisord -c /app/supervisord.conf