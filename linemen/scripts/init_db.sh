#!/usr/bin/env bash

bash wait-for-it.sh db:5432 -- flask db upgrade
flask init-db