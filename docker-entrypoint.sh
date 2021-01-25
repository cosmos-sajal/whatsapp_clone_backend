#!/bin/bash

s4cmd get s3://whatsapp-clone-bucket/serviceAccount.json /serviceAccount.json
s4cmd get s3://	whatsapp-clone-bucket/secrets.py /app/app/secrets.py

exec "$@"
