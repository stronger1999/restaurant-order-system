#!/bin/sh
set -e

if [ -n "$DB_HOST" ]; then
  echo "Waiting for database at $DB_HOST:$DB_PORT..."
  until nc -z "$DB_HOST" "${DB_PORT:-3306}"; do
    sleep 1
  done
fi

exec "$@"
