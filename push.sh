#!/bin/bash

clear
set -ex

git config --global user.name "goofy"
git config --global user.email "goofy@rickroll.com"

while true; do
    files=$(git ls-files --others --exclude-standard | head -10)
    if [ -z "$files" ]; then
        break
    fi
    git add $files
    git commit -m "Chore: Add part files"
    git push
done
