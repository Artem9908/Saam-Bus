#!/bin/bash
export TESTING=true
export DATABASE_URL="sqlite:///:memory:"
export REDIS_HOST="localhost"
export REDIS_PORT=6379
export REDIS_DB=0
export SKIP_GOOGLE_AUTH=true

pytest "$@"