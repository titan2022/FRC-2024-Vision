#!/bin/bash

# This script will set up FRC-2024-Vision to be autostarted on the Jetson.

# Disable the desktop
sudo systemctl set-default multi-user.target

sudo mkdir -p 

cat <<EOF | sudo tee /etc/systemd/system/titan2022.service
[Unit]
Description=Titan2022
After=network.target

[Service]
Type=simple
ExecStart=/home/titan/Projects/FRC-2024-Vision/titan2022-service.sh
Restart=on-failure
RestartSec=1
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

sudo chmod 640 /etc/systemd/system/titan2022.service
sudo systemctl daemon-reload
sudo systemctl enable titan2022
