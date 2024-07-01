#!/bin/sh
set -e

python -m app.PoolAccessMqttBridge --config=/data/options.json --sensors=/data/sensors.json
