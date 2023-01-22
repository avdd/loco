#!/bin/bash -eu

JSON_URL='https://api.github.com/repos/mozilla/geckodriver/releases/latest'
LOCAL_BIN=$HOME/.local/bin

set -x

mkdir -p "$LOCAL_BIN"
url=$(curl -s "$JSON_URL" | grep -o 'https.*linux64.tar.gz' | head -1)
curl -sL "$url" | zcat - | tar -C "$LOCAL_BIN" -xf-
