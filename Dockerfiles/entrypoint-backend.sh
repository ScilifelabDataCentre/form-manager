#!/bin/bash

# Exit on error and treat unset variables as errors
# (see https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)
set -eu

# Run webserver -- `exec` let the webserver become the container's PID 1 to handle Unix signals correctly
# (see https://docs.docker.com/build/building/best-practices/#entrypoint)
exec gunicorn app:app --bind 0.0.0.0:8000 --workers 2 --threads 4 --worker-class gthread --worker-tmp-dir /dev/shm --forwarded-allow-ips='*' --access-logfile -

# Run additional commands
exec "$@"
