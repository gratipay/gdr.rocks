#!/usr/bin/env bash
set -e

cd /root/gdr.rocks

git pull
env/bin/pip install --upgrade -r requirements.txt
crontab crontab
docker build -t gdr .
