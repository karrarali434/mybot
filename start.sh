#!/bin/bash

echo "=== Installing system dependencies ==="
sudo apt-get update
sudo apt-get install -y ffmpeg redis-server

echo "=== Starting Redis ==="
sudo service redis-server start

echo "=== Installing Python dependencies ==="
python3 -m pip install -r requirements.txt

echo "=== Starting the bot ==="
python3 main.py
