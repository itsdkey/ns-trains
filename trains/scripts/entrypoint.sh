#!/bin/sh

celery -A src worker \
  --beat \
  --loglevel=info \
  --concurrency=2 \
  --without-gossip \
  --without-heartbeat \
  --without-mingle