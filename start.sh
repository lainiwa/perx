#!/usr/bin/env bash

set -o errexit  # exit on fail
set -o pipefail # catch errors in pipelines
set -o nounset  # exit on undeclared variable
# set -o xtrace    # trace execution

# Run server
PERX_WORKERS_NUM=2 \
    poetry run python src/perx/ &

# Wait for server to bootstrap
while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:8000/peek)" != "200" ]]; do sleep 0.1; done

# Create some tasks
http POST :8000/enqueue n==10 d==1 interval==2
http POST :8000/enqueue n==10 d==2 interval==2
http POST :8000/enqueue n==10 d==3 interval==2

# Continuously touch endpoint
while true; do
    http :8000/peek
    sleep 1
done

# Wait for server to exit
wait $(jobs -rp)
