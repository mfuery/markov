#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

cmd="$@"

# Here, do any prechecks to starting the gunicorn WSGI, like checking for DB
# connectivity, check that other required services are up, etc.



# Proceed with starting the HTTP server, or running cmd if specified.
if [[ -z "${cmd}" ]]; then
  /gunicorn.sh
else
  ${cmd}
fi

echo "End of entrypoint.sh at $(date)"
