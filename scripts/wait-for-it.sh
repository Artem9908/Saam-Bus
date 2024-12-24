#!/bin/bash
# wait-for-it.sh

set -e

host=$(echo $1 | cut -d: -f1)
port=$(echo $1 | cut -d: -f2)

shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd 