#!/bin/sh
set -e

python manage.py migrate --noinput

python manage.py create_admin

python manage.py collectstatic --noinput

exec supervisord -c /app/supervisord.conf