#!/bin/sh

chown -R worker:worker /home/worker/db
exec runuser -u worker "$@"
