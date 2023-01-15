#!/usr/bin/env bash
apt update -yq
apt install -y rclone python3-pydantic python3-yaml python3-fire python3-coloredlogs ca-certificates

cp -r /config/rclone /root/.config

python3 /tools/backups.py status
