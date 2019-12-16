#!/bin/bash

while true; do
    alembic upgrade head
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

exec gunicorn -b 0.0.0.0:5000 -w 1 --threads 2 --log-level info wsgi:app