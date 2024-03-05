#!/bin/sh

set -e

uwsgi \
    --socket :${APP_PORT} \
    --wsgi-file app.py \
    --callable app \
    --processes 4 \
    --threads 10 \
    --master \
    --log-x-forwarded-for \
    --log-prefix=uwsgi \
    --harakiri 60 \
    --thunder-lock \
    --vacuum \
    --max-requests 1000 \
    --lazy-apps