#!/usr/bin/env bash
set -e

cd /root/

git fetch

# http://stackoverflow.com/a/3278427
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
BASE=$(git merge-base @ @{u})

if [ $LOCAL = $REMOTE ]; then
    exit 0
elif [ $LOCAL = $BASE ]; then
    echo "Here we go!"
    exec ./update.sh
elif [ $REMOTE = $BASE ]; then
    echo "WTF? Need to push."
    exit 1
else
    echo "WTF? Diverged."
    exit 1
fi
