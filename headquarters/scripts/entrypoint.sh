#!/bin/sh

celery -A src worker \
  --loglevel=info \
  --concurrency=4 \
  --without-gossip \
  --without-heartbeat \
  --without-mingle