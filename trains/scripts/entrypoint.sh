#!/bin/sh

celery -A src worker --beat --loglevel=info