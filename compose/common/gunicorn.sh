#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

cd /app

# Start Gunicorn processes
echo Starting Gunicorn.
gunicorn config.wsgi:application \
    --name dadjokes \
    --workers 3 \
    --log-level ${DJANGO_LOG_LEVEL} \
    --log-file - \
    --access-logfile - \
    --timeout 900 \
    -k gevent \
    -b 0.0.0.0:8000
