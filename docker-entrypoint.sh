#!/bin/sh
set -e

# ------------------------------------------------------------------
# Wait for PostgreSQL (when DB_HOST is set and not SQLite)
# ------------------------------------------------------------------
if [ "${DB_ENGINE:-sqlite}" = "postgresql" ] && [ -n "${DB_HOST}" ]; then
  echo "Waiting for PostgreSQL at ${DB_HOST}:${DB_PORT:-5432}..."
  while ! nc -z "${DB_HOST}" "${DB_PORT:-5432}" 2>/dev/null; do
    sleep 1
  done
  echo "PostgreSQL is ready."
fi

# ------------------------------------------------------------------
# Django setup
# ------------------------------------------------------------------
python manage.py migrate --noinput

python manage.py loaddata demo.json 2>/dev/null || true

if [ -n "${DJANGO_SUPERUSER_USERNAME}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ]; then
  python manage.py createsuperuser \
    --username="${DJANGO_SUPERUSER_USERNAME}" \
    --email="${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" \
    --noinput 2>/dev/null || true
fi

exec "$@"
