#!/bin/sh
set -e
cd /
python -m app.PoolAccessMqttBridge --config=/data/options.json --sensors=/app/sensors.json
