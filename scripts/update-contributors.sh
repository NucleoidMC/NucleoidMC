#!/usr/bin/env bash

cd contributors/
echo 'Fetching contributors from Discord...'
python3 fetch-contributors-discord.py
cd ../

echo 'Rendering new README...'
python3 contributors/build-readme.py contributors/contributors.discord.json contributors/README.template.md
