#!/bin/bash

clear
set -ex

git config --global user.name "goofy"
git config --global user.email "goofy@rickroll.com"

for i in {1..9}
do
    git add */part$i* || continue
    git commit -m "Chore: Add part$i files" || continue
    git push || continue
done