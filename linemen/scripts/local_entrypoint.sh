#!/bin/sh

set -e

flask run --debug -h 0.0.0.0 -p $APP_PORT