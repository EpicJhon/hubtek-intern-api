#!/bin/sh

python -u /home/worker/main.py &
celery -A tasks.tasks worker --loglevel=INFO &
wait
