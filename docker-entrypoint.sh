#!/bin/sh
if [ -z "$DISCOURSE_URL" ] ; then
  echo "DISCOURSE_URL environment variable must be set. Exiting."
  exit 1
fi
/usr/bin/python /app/main.py
crond -f