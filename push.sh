#!/bin/bash

clear
set -ex

git config --global user.name "goofy"
git config --global user.email "goofy@rickroll.com"

files=$(git ls-files --others --exclude-standard | head -10)
if [ -n "$files" ]; then
    git add $files
    git commit -m "Chore: Add part files"
    git push
fi
