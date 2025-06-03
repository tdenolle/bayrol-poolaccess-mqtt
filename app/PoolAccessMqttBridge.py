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
import sys
import threading
import time

from docopt import docopt
from paho.mqtt.client import MQTTMessage, MQTT_ERR_SUCCESS

from app.hass import HASS_ENTITY_TYPES
from app.Translation import LanguageManager
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity
from app.mqtt.MqttClient import MqttClient
from app.mqtt.PoolAccessClient import PoolAccessClient, PoolAccessTopicMode

DEFAULT_RECONNECT_DELAY = 30

class PoolAccessMqttBridge:
    _logger = None
    _poolaccess_client = None
    _broker_client = None

    def __init__(self,
                 mqtt_base_topic: str,
                 poolaccess_device_serial: str,
                 hass_entities: list[Entity],
                 poolaccess_client: PoolAccessClient,
                 broker_client: MqttClient):
        # Logger
        self._logger = logging.getLogger()
        self._reconnect_delay = DEFAULT_RECONNECT_DELAY
        # Mqtt base topic
        self._mqtt_base_topic = mqtt_base_topic
        # Home Assistant Entities
        self._hass_entities = hass_entities
        # Mqtt Clients
        self._poolaccess_client = poolaccess_client
        self._broker_client = broker_client
        # Device Serial
        self._poolaccess_device_serial = poolaccess_device_serial

    def on_poolaccess_message(self, client: PoolAccessClient, userdata, message: MQTTMessage):
        if not message or message.payload is None or message.topic is None:
            return
        self._logger.debug("[poolaccess] message [%s][%s]", str(message.topic), str(message.payload))
        for e in self._hass_entities:  # type: Entity
            e.on_poolaccess_message(self._poolaccess_client, self._broker_client, message)

    def on_poolaccess_connect(self, client: PoolAccessClient, userdata, flags, rc, properties):
        if rc == 0:
            self._logger.info("[poolaccess] connect: [%s][%s][%s]", str(rc), str(userdata), str(flags))
            # Subscribing to PoolAccess Messages
            dash_topic = self._poolaccess_client.build_topic(PoolAccessTopicMode.VALUE, "#")
            self._logger.info("Subscribing to topic: %s", dash_topic)
            self._poolaccess_client.subscribe(dash_topic)

            # Resetting broker config to remove old entities
            for e in list(filter(lambda entity: entity.disable, self._hass_entities)) :
                (topic, cfg) = e.build_config()
                self._logger.info("Removing broker config for topic: %s", topic)
                self._broker_client.publish(topic, payload=None, retain=True)

            # Looping on active entities
            for e in list(filter(lambda entity: not entity.disable, self._hass_entities)) :  # type: Entity
                # Publish entity config to Broker
                (topic, cfg) = e.build_config()
                payload = str(json.dumps(cfg))
                self._logger.info("Publishing to broker: %s %s", topic, payload)
                self._broker_client.publish(topic, payload=payload, retain=True)

                # Trigger on_poolaccess_connect for each entity
                e.on_poolaccess_connect(client)
        else:
            self._logger.info("[poolaccess] connect: Connection failed [%s]", str(rc))
            exit(1)

    def on_broker_connect(self, client: MqttClient, userdata, flags, rc, properties):
        if rc == 0:
            self._logger.info("[mqtt] connect: [%s][%s][%s]", str(rc), str(userdata), str(flags))


            # Looping on active entities
            for e in list(filter(lambda entity: not entity.disable, self._hass_entities)):  # type: Entity
                e.on_broker_connect(client)
        else:
            self._logger.info("[mqtt] connect: Connection failed [%s]", str(rc))
            exit(1)

    def on_broker_message(self, client: MqttClient, userdata, message: MQTTMessage):
        self._logger.info("[mqtt] message [%s][%s]", str(message.topic), str(message.payload))
        # Stop if no message or payload
        if not (message
                and message.payload
                and message.topic):
            return

        # Trigger on_broker_message for each active entity
        for e in list(filter(lambda e: not e.disable, self._hass_entities)):  # type: Entity
            e.on_broker_message(self._poolaccess_client, self._broker_client, message)

    def on_disconnect(self, client, userdata, flags, rc, properties):
        self._logger.warning("[mqtt] disconnect: %s  [%s][%s][%s]", type(client).__name__, str(rc), str(userdata),
                             str(flags))

    def _multi_loop(self, loop=True, timeout=1):
        while True:
            broker_status = self._broker_client.loop(timeout)
            poolaccess_status = self._poolaccess_client.loop(timeout)

            if broker_status != MQTT_ERR_SUCCESS:
                self._logger.warning("Broker Client has been disconnected [status: %s] : trying to reconnect ...",
                                     broker_status)
                try:
                    self._broker_client.reconnect()
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

        # Broker setup
        self._broker_client.on_connect = self.on_broker_connect
        self._broker_client.on_message = self.on_broker_message
        self._broker_client.on_disconnect = self.on_disconnect
        if self._broker_client.establish_connection() != 0:
            self._logger.error("MQTT Brocker connection failure !")
            connection_success = False

        # Multithreading startup if connection_success
        if connection_success:
            self._logger.info("Starting Multithreading")
            t = threading.Thread(target=self._multi_loop, args=())  # start multi loop
            t.start()


def load_entities(filepath: str, config) -> []:
    if "DEVICE_SERIAL" not in config:
        raise KeyError("DEVICE_SERIAL option can not be found in configuration.")
    device = BayrolPoolaccessDevice(config["DEVICE_SERIAL"])
    hass_discovery_prefix = config["HASS_DISCOVERY_PREFIX"] if "HASS_DISCOVERY_PREFIX" in config else "homeassistant"
    entities = []
    with open(filepath, 'r') as fp:
        content = fp.read()
        # Replace config value in entities file
        for k in config:
            content = content.replace("#%s" % k, str(config[k]))
        # Instantiate entities
        for e in json.loads(content):
            # default class type is Sensor
            class_type = "Sensor"
            if "__class__" in e:
                class_type = e["__class__"]
                del e["__class__"]
            # Load module
            hass_module = importlib.import_module("app.hass.%s" % class_type)
            # Get class
            hass_class = getattr(hass_module, class_type)
            # Instantiate the class (pass arguments to the constructor, if needed)
            entities.append(hass_class(e, device, hass_discovery_prefix))
    return entities


def main(config: dict):
    LanguageManager().setup(config["LANGUAGE"] if "LANGUAGE" in config else "fr")
    broker = MqttClient(config["MQTT_HOST"], config["MQTT_PORT"],
                        config["MQTT_USER"] if "MQTT_USER" in config else None,
                        config["MQTT_PASSWORD"] if "MQTT_PASSWORD" in config else None)
    poolaccess_client = PoolAccessClient(config["DEVICE_TOKEN"], config["DEVICE_SERIAL"])
    hass_entities = load_entities(os.path.join(os.path.dirname(__file__), "entities.json"), config)
    logger = logging.getLogger()
    logger.info("Starting Bridge")
    bridge = PoolAccessMqttBridge(
        config["MQTT_BASE_TOPIC"],
        config["DEVICE_SERIAL"],
        hass_entities,
        poolaccess_client,
        broker
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
