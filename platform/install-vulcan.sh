#!/bin/bash

set -e

echo "Installing vulcan via pip..."
pip install vulcan

echo "Downloading vulcan-skill.zip..."
wget -O /tmp/vulcan-skill.zip https://sd6f6o1jtvotb9m1jclvg.apigateway-cn-beijing.volceapi.com/vulcan-skill.zip

echo "Creating target directory..."
mkdir -p /home/gem/openclaw/skills/vulcan-skill

echo "Unzipping file..."
unzip -o /tmp/vulcan-skill.zip -d /home/gem/openclaw/skills/vulcan-skill

echo "Cleaning up..."
rm -f /tmp/vulcan-skill.zip

echo "Installation completed successfully!"