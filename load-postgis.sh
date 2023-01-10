#!/bin/sh

# A script to be run after creating the DB that will create the postgis extension

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<EOF
create extension postgis;
EOF