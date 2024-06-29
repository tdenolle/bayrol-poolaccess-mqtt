#!/bin/sh
set -e

python3 /app/PoolAccessMqttBridge.py --config=/data/options.json --sensors=/data/sensors.json
