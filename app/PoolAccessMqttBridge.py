#!/usr/bin/env python3

""" Home Assistant MQTT bridge

Usage:
    PoolAccessMqttBridge [--config=<file>] [--debug]

Options:
    -c <file>, --config=<file>          Config file path [default: options.json]
    --debug                             Debug mode
    --help                              Display Help

"""

import importlib
import json
import logging
import os
import re
import threading
import sys
import time

from docopt import docopt
from paho.mqtt.client import MQTTMessage, MQTT_ERR_SUCCESS

from .hass.Entity import Entity
from .utils.Utils import get_device_model_from_serial
from .hass.Sensor import Sensor
from .hass.MessagesSensor import MessagesSensor
from .mqtt.MqttClient import MqttClient
from .mqtt.PoolAccessClient import PoolAccessClient

DEFAULT_RECONNECT_DELAY = 30


class PoolAccessMqttBridge:
    _logger = None
    _poolaccess_client = None
    _brocker_client = None

    def __init__(self,
                 mqtt_base_topic: str,
                 poolaccess_device_serial: str,
                 hass_discovery_prefix: str,
                 hass_entities: list[Entity],
                 poolaccess_client: PoolAccessClient,
                 brocker_client: MqttClient):
        # Logger
        self._logger = logging.getLogger()
        self._reconnect_delay = DEFAULT_RECONNECT_DELAY
        # Poolaccess Device Serial
        self._poolaccess_device_serial = poolaccess_device_serial
        # Mqtt base topic
        self._mqtt_base_topic = mqtt_base_topic
        # Home Assistant Discovery Prefix
        self._hass_discovery_prefix = hass_discovery_prefix
        # Home Assistant Entities
        self._hass_entities = hass_entities
        # Mqtt Clients
        self._poolaccess_client = poolaccess_client
        self._brocker_client = brocker_client

    def on_poolaccess_message(self, client: PoolAccessClient, userdata, message: MQTTMessage):
        self._logger.debug("[poolaccess] message [%s]", str(message.topic))
        for e in self._hass_entities:  # type: Entity
            if re.match(".+/v/%s$" % e.uid, message.topic):
                self._logger.debug("Reading %s %s", message.topic, str(message.payload))
                payload = e.get_payload(message.payload)
                topic = self.get_entity_topic(e)
                self._brocker_client.publish(topic, payload, message.qos, retain=True)
                self._logger.info("Publishing to brocker %s %s", topic, str(payload))

    def on_poolaccess_connect(self, client: PoolAccessClient, userdata, flags, rc, properties):
        if rc == 0:
            self._logger.info("[poolaccess] connect: [%s][%s][%s]", str(rc), str(userdata), str(flags))
            device = {
                "identifiers": [self._poolaccess_device_serial],
                "manufacturer": "Bayrol",
                "model": get_device_model_from_serial(self._poolaccess_device_serial),
                "name": "Bayrol %s" % self._poolaccess_device_serial
            }

            # Subscribing to PoolAccess Messages
            topic = "d02/%s/v/#" % self._poolaccess_device_serial
            self._logger.info("Subscribing to topic: %s", topic)
            self._poolaccess_client.subscribe(topic, qos=1)

            # Looping on sensors
            for s in self._hass_entities:  # type: Entity
                # Publish entity config to Brocker
                (topic, cfg) = s.build_config(device, self._hass_discovery_prefix)
                payload = str(json.dumps(cfg))
                self._logger.info("Publishing to brocker: %s %s", topic, payload)
                self._brocker_client.publish(topic, qos=1, payload=payload, retain=True)

                # Publish Get topic to Poolaccess
                topic = "d02/%s/g/%s" % (self._poolaccess_device_serial, s.uid)
                self._logger.info("Publishing to poolaccess: %s", topic)
                self._poolaccess_client.publish(topic, qos=0, payload=s.get_payload())
        else:
            self._logger.info("[poolaccess] connect: Connection failed [%s]", str(rc))
            exit(1)

    def on_brocker_connect(self, client: MqttClient, userdata, flags, rc, properties):
        if rc == 0:
            self._logger.info("[mqtt] connect: [%s][%s][%s]", str(rc), str(userdata), str(flags))
        else:
            self._logger.info("[mqtt] connect: Connection failed [%s]", str(rc))
            exit(1)

    def on_brocker_message(self, client: MqttClient, userdata, message: MQTTMessage):
        self._logger.info("[mqtt] message [%s][%s]", str(message.topic), str(message.payload))
        # only dealing with set commands
        if not message.topic.endswith("/set"):
            return
        # finding corresponding entity and publishing to poolaccess client
        for e in self._hass_entities:  # type: Entity
            if re.match(".+/%s/set$" % e.key, message.topic):
                poolaccess_topic = "d02/%s/s/%s" % (self._poolaccess_device_serial, e.uid)
                self._logger.info("Publishing to poolaccess: %s", poolaccess_topic)
                self._poolaccess_client.publish(poolaccess_topic, qos=0, payload=message.payload, retain=True)

    def on_disconnect(self, client, userdata, flags, rc, properties):
        self._logger.warning("[mqtt] disconnect: %s  [%s][%s][%s]", type(client).__name__, str(rc), str(userdata),
                             str(flags))

    def _multi_loop(self, loop=True, timeout=1):
        while True:
            brocker_status = self._brocker_client.loop(timeout)
            poolaccess_status = self._poolaccess_client.loop(timeout)

            if brocker_status != MQTT_ERR_SUCCESS:
                self._logger.warning("Brocker Client has been disconnected [status: %s] : trying to reconnect ...",
                                     brocker_status)
                try:
                    self._brocker_client.reconnect()
                except Exception as e:
                    self._logger.error("Reconnect exception occurred %s ...", str(e))
                self._logger.info("Waiting %ss ...", str(self._reconnect_delay))
                time.sleep(self._reconnect_delay)

            if poolaccess_status != MQTT_ERR_SUCCESS:
                self._logger.warning("Poolaccess Client has been disconnected [status: %s] : trying to reconnect ...",
                                     poolaccess_status)
                try:
                    self._poolaccess_client.reconnect()
                except Exception as e:
                    self._logger.error("Reconnect exception occurred %s ...", str(e))
                self._logger.info("Waiting %ss ...", str(self._reconnect_delay))
                time.sleep(self._reconnect_delay)

            # loop exit condition
            if not loop:
                break

    def start(self):
        connection_success = True
        # PoolAccess setup
        self._poolaccess_client.on_message = self.on_poolaccess_message
        self._poolaccess_client.on_connect = self.on_poolaccess_connect
        self._poolaccess_client.on_disconnect = self.on_disconnect
        if self._poolaccess_client.establish_connection() != 0:
            self._logger.error("Poolaccess connection failure !")
            connection_success = False

        # Brocker setup
        self._brocker_client.on_connect = self.on_brocker_connect
        self._brocker_client.on_disconnect = self.on_disconnect
        if self._brocker_client.establish_connection() != 0:
            self._logger.error("MQTT Brocker connection failure !")
            connection_success = False

        # Multithreading startup if connection_success
        if connection_success:
            self._logger.info("Starting Multithreading")
            t = threading.Thread(target=self._multi_loop, args=())  # start multi loop
            t.start()

    def get_entity_topic(self, entity: Entity):
        return "%s/%s/%s/%s" % (self._hass_discovery_prefix, entity.type, self._poolaccess_device_serial, entity.key)


def load_entities(filepath: str) -> []:
    entities = []
    with open(filepath, 'r') as fp:
        for s in json.load(fp):
            class_type = "Sensor"
            if "__class__" in s :
                class_type = s["__class__"]
                del s["__class__"]
            # Load module
            hass_module = importlib.import_module("app.hass.%s" % class_type)
            # Get class
            hass_class = getattr(hass_module, class_type)
            # Instantiate the class (pass arguments to the constructor, if needed)
            entities.append(hass_class(s))
    return entities


def main(config: dict):
    brocker_client = MqttClient(config["MQTT_HOST"], config["MQTT_PORT"], config["MQTT_USER"], config["MQTT_PASSWORD"])
    poolaccess_client = PoolAccessClient(config["DEVICE_TOKEN"])
    hass_entities = load_entities(os.path.join(os.path.dirname(__file__), "entities.json"))
    logger = logging.getLogger()
    logger.info("Starting Bridge")
    bridge = PoolAccessMqttBridge(
        config["MQTT_BASE_TOPIC"],
        config["DEVICE_SERIAL"],
        config["HASS_DISCOVERY_PREFIX"],
        hass_entities,
        poolaccess_client,
        brocker_client
    )
    bridge.start()


if __name__ == "__main__":
    args = docopt(__doc__)
    # Config load
    with open(args['--config'], 'r') as f:
        c = json.load(f)

    # Logger
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s :: %(levelname)s :: %(message)s')
    logging.getLogger().setLevel('DEBUG' if args['--debug'] else c["LOG_LEVEL"])

    main(c)
