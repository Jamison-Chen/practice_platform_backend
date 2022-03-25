#!/bin/bash
if [[ -z $1 ]]; then
    echo Please provide the commit message.
else
    pipenv lock --requirements > requirements.txt
    git checkout development
    git add .
    git commit -m "$1"
    git push origin development
fi