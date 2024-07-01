#!/usr/bin/env python3

""" Home Assistant MQTT bridge

Usage:
    PoolAccessMqttBridge [--config=<file>] [--sensors=<file>] [--debug]

Options:
    -c <file>, --config=<file>          Config file path [default: options.json]
    -s <file>, --sensors=<file>         Sensors file path [default: sensors.json]
    --debug                             Debug mode
    --help                              Display Help

"""

import json
import logging
import re
import threading
import sys
from docopt import docopt
from paho.mqtt.client import MQTTMessage

from .hass.Sensor import Sensor
from .hass.Sensor import load_sensors
from .mqtt.MqttClient import MqttClient
from .mqtt.PoolAccessClient import PoolAccessClient


class PoolAccessMqttBridge:
    _logger = None
    _poolaccess_client = None
    _brocker_client = None

    def __init__(self,
                 mqtt_base_topic: str,
                 poolaccess_device_serial: str,
                 hass_discovery_prefix: str,
                 hass_sensors: list[Sensor],
                 poolaccess_client: PoolAccessClient,
                 brocker_client: MqttClient):
        # Logger
        self._logger = logging.getLogger()
        # Poolaccess Device Serial
        self._poolaccess_device_serial = poolaccess_device_serial
        # Mqtt base topic
        self._mqtt_base_topic = mqtt_base_topic
        # Home Assistant Discovery Prefix
        self._hass_discovery_prefix = hass_discovery_prefix
        # Base sensor topic
        self._base_sensor_topic = "%s/sensor/%s" % (hass_discovery_prefix, poolaccess_device_serial)
        # Home Assistant Sensors
        self._hass_sensors = hass_sensors
        # Mqtt Clients
        self._poolaccess_client = poolaccess_client
        self._brocker_client = brocker_client

    def on_poolaccess_message(self, client: PoolAccessClient, userdata, message: MQTTMessage):
        self._logger.debug("[poolaccess] on_message: [%s] %s", str(userdata), str(message.topic))
        for s in self._hass_sensors:  # type: Sensor
            if re.match(".+/v/%s$" % s.uid, message.topic):
                self._logger.debug("Reading %s %s", message.topic, str(message.payload))
                payload = s.payload if s.payload else message.payload
                topic = "%s/%s" % (self._base_sensor_topic, s.key)
                self._brocker_client.publish(topic, payload, message.qos, retain=True)
                self._logger.debug("Publishing to brocker %s %s", topic, str(payload))

    def on_poolaccess_connect(self, client: PoolAccessClient, userdata, flags, rc, properties):
        if rc == 0:
            self._logger.info("[poolaccess] on_connect: [%s][%s][%s]", str(rc), str(userdata), str(flags))
            device = {
                "identifiers": [self._poolaccess_device_serial],
                "manufacturer": "Bayrol",
                "model": "Automatic Salt" if "AS" in self._poolaccess_device_serial else "Unknown",
                "name": "Bayrol %s" % self._poolaccess_device_serial
            }

            # Subscribing to PoolAccess Messages
            topic = "d02/%s/v/#" % self._poolaccess_device_serial
            self._logger.info("Subscribing to topic: %s", topic)
            self._poolaccess_client.subscribe(topic, qos=1)

            # Looping on sensors
            for s in self._hass_sensors:  # type: Sensor
                # Publish Get topic to Poolaccess
                topic = "d02/%s/g/%s" % (self._poolaccess_device_serial, s.uid)
                self._logger.info("Publishing to poolaccess: %s", topic)
                self._poolaccess_client.publish(topic, qos=0, payload=s.payload)

                # Publish sensor config to brocker
                (topic, cfg) = s.build_config(device, self._hass_discovery_prefix)
                payload = str(json.dumps(cfg))
                self._logger.info("Publishing to brocker: %s %s", topic, payload)
                self._brocker_client.publish(topic, qos=1, payload=payload, retain=True)
        else:
            self._logger.info("[poolaccess] on_connect: Connection failed [%s]", str(rc))
            exit(1)

    def on_brocker_connect(self, client: MqttClient, userdata, flags, rc, properties):
        if rc == 0:
            self._logger.info("[mqtt] on_connect: [%s][%s][%s]", str(rc), str(userdata), str(flags))
        else:
            self._logger.info("[mqtt] on_connect: Connection failed [%s]", str(rc))
            exit(1)

    def _multi_loop(self, timeout=1):
        while True:
            self._brocker_client.loop(timeout)
            self._poolaccess_client.loop(timeout)

    def start(self):
        # PoolAccess setup
        self._poolaccess_client.on_message = self.on_poolaccess_message
        self._poolaccess_client.on_connect = self.on_poolaccess_connect
        self._poolaccess_client.establish_connection()
        # Brocker setup
        self._brocker_client.on_connect = self.on_brocker_connect
        self._brocker_client.establish_connection()
        # Multithreading startup
        t = threading.Thread(target=self._multi_loop, args=())  # start multi loop
        t.start()


def main():
    brocker_client = MqttClient(config["MQTT_HOST"], config["MQTT_PORT"], config["MQTT_USER"], config["MQTT_PASSWORD"])
    poolaccess_client = PoolAccessClient(config["DEVICE_TOKEN"])
    hass_sensors = load_sensors(arguments['--sensors'])
    bridge = PoolAccessMqttBridge(
        config["MQTT_BASE_TOPIC"],
        config["DEVICE_SERIAL"],
        config["HASS_DISCOVERY_PREFIX"],
        hass_sensors,
        poolaccess_client,
        brocker_client
    )
    bridge.start()


if __name__ == "__main__":
    arguments = docopt(__doc__)
    # Config load
    with open(arguments['--config'], 'r') as f:
        config = json.load(f)

    # Logger
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')
    logger = logging.getLogger()
    logger.setLevel('DEBUG' if arguments['--debug'] else config["LOG_LEVEL"])

    main()
