#!/bin/sh
if [ -z "$DISCOURSE_URL_BASE" ] ; then
  echo "DISCOURSE_URL_BASE environment variable must be set. Exiting."
  exit 1
fi
/usr/bin/python /app/main.py
crond -f