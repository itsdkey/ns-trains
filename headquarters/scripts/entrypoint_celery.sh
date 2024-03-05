#!/bin/sh

celery -A src.celery worker --concurrency=4 --loglevel=info