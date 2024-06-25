#!/bin/sh
set -e

CONFIG_PATH=/data/options.json

python3 /app/PoolAccessMqttBridge.py --config=$CONFIG_PATH
