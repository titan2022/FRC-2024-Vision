#!/bin/bash

cd ~/Projects/FRC-2024-Vision/src
source ~/.venvs/FRC-2024-Vision/bin/activate
echo "titan2022.service: Starting..." | systemd-cat -p info
python3 example-realsense.py | systemd-cat -p info
