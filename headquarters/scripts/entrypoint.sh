#!/bin/sh

celery -A src worker --concurrency=4 --loglevel=info