#!/bin/sh
set -e

python manage.py migrate --noinput

python manage.py loaddata demo.json 2>/dev/null || true

if [ -n "${DJANGO_SUPERUSER_USERNAME}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ]; then
  python manage.py createsuperuser \
    --username="${DJANGO_SUPERUSER_USERNAME}" \
    --email="${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
    --noinput 2>/dev/null || true
fi

exec "$@"
