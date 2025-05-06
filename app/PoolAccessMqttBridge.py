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
from json import JSONDecodeError

from docopt import docopt
from paho.mqtt.client import MQTTMessage, MQTT_ERR_SUCCESS

from app.Translation import LanguageManager
from .hass.Switch import Switch
from .hass.Climate import Climate
from .hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from .hass.Entity import Entity
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
                 hass_entities: list[Entity],
                 poolaccess_client: PoolAccessClient,
                 brocker_client: MqttClient):
        # Logger
        self._logger = logging.getLogger()
        self._reconnect_delay = DEFAULT_RECONNECT_DELAY
        # Mqtt base topic
        self._mqtt_base_topic = mqtt_base_topic
        # Home Assistant Entities
        self._hass_entities = hass_entities
        # Mqtt Clients
        self._poolaccess_client = poolaccess_client
        self._brocker_client = brocker_client
        # Device Serial
        self._poolaccess_device_serial = poolaccess_device_serial

    def on_poolaccess_message(self, client: PoolAccessClient, userdata, message: MQTTMessage):
        if not message or message.payload is None or message.topic is None:
            return
        self._logger.debug("[poolaccess] message [%s][%s]", str(message.topic), str(message.payload))
        for e in self._hass_entities:  # type: Entity
            if re.match(".+/v/%s$" % e.uid, message.topic):
                self._logger.info("Reading %s %s", message.topic, str(message.payload))
                try:
                    payload = e.get_payload(message.payload)
                    self._brocker_client.publish(e.state_topic, payload, message.qos, retain=True)
                    self._logger.info("Publishing to brocker %s %s", e.state_topic, str(payload))
                except JSONDecodeError as e:
                    self._logger.error(e)
            if hasattr(e, 'uid_mode') and re.match(".+/v/%s$" % e.uid_mode, message.topic):
                self._logger.info("Reading %s %s", message.topic, str(message.payload))
                try:
                    payload = e.get_payload(message.payload)
                    self._brocker_client.publish(e.state_topic, payload, message.qos, retain=True)
                    self._logger.info("Publishing to brocker %s %s", e.state_topic, str(payload))
                except JSONDecodeError as e:
                    self._logger.error(e)

            if hasattr(e, 'uid_temp') and re.match(".+/v/%s$" % e.uid_temp, message.topic):
                self._logger.info("Reading %s %s", message.topic, str(message.payload))
                try:
                    payload = e.get_payload(message.payload)
                    self._brocker_client.publish(e.state_topic, payload, message.qos, retain=True)
                    self._logger.info("Publishing to brocker %s %s", e.state_topic, str(payload))
                except JSONDecodeError as e:
                    self._logger.error(e)

    def on_poolaccess_connect(self, client: PoolAccessClient, userdata, flags, rc, properties):
        if rc == 0:
            self._logger.info("[poolaccess] connect: [%s][%s][%s]", str(rc), str(userdata), str(flags))
            # Subscribing to PoolAccess Messages
            topic = "d02/%s/v/#" % self._poolaccess_device_serial
            self._logger.info("Subscribing to topic: %s", topic)
            self._poolaccess_client.subscribe(topic)

            # Looping on entities
            for e in self._hass_entities:  # type: Entity
                # Publish entity config to Brocker
                (topic, cfg) = e.build_config()
                payload = str(json.dumps(cfg))
                self._logger.info("Publishing to brocker: %s %s", topic, payload)
                self._brocker_client.publish(topic, payload=payload, retain=True)

                # Publish Get topic to Poolaccess
                topic = "d02/%s/g/%s" % (self._poolaccess_device_serial, e.uid)
                self._logger.info("Publishing to poolaccess: %s", topic)
                self._poolaccess_client.publish(topic, payload=e.get_payload())
        else:
            self._logger.info("[poolaccess] connect: Connection failed [%s]", str(rc))
            exit(1)

    def on_brocker_connect(self, client: MqttClient, userdata, flags, rc, properties):
        if rc == 0:
            self._logger.info("[mqtt] connect: [%s][%s][%s]", str(rc), str(userdata), str(flags))
            # Looping on entities
            for e in self._hass_entities:  # type: Entity
                if isinstance(e, Switch):
                    # Subscribing to Entity Messages
                    self._logger.info("Subscribing to topic: %s", e.command_topic)
                    self._brocker_client.subscribe(e.command_topic)
                if isinstance(e, Climate):
                    # Subscribing to Entity Messages
                    self._logger.info("Subscribing to topic: %s", e.temperature_command_topic)
                    self._brocker_client.subscribe(e.temperature_command_topic)
                    self._logger.info("Subscribing to topic: %s", e.mode_command_topic)
                    self._brocker_client.subscribe(e.mode_command_topic)
        else:
            self._logger.info("[mqtt] connect: Connection failed [%s]", str(rc))
            exit(1)

    def on_brocker_message(self, client: MqttClient, userdata, message: MQTTMessage):
        self._logger.info("[mqtt] message [%s][%s]", str(message.topic), str(message.payload))
        # only dealing with set commands
        if not (message
                and message.payload
                and message.topic):
            return
        # finding corresponding entity and publishing to poolaccess client

        for e in self._hass_entities:  # type: Entity
            topic_brocker = None
            topic_poolaccess = None
            payload = message.payload
            if re.match(".+/%s/set$" % e.key, message.topic):
                topic_brocker = e.state_topic
                topic_poolaccess = "d02/%s/s/%s" % (self._poolaccess_device_serial, e.uid)

            if re.match(".+/%s/set_temp$" % e.key, message.topic):
                topic_brocker = e.temperature_command_topic
                topic_poolaccess = "d02/%s/s/%s" % (self._poolaccess_device_serial, e.uid_temp)
                
            if re.match(".+/%s/set_mode$" % e.key, message.topic):
                topic_brocker = e.mode_command_topic
                topic_poolaccess = "d02/%s/s/%s" % (self._poolaccess_device_serial, e.uid_mode)
                
            if topic_brocker is not None:
                 # Publish data to brocker to persist it
                self._logger.info("Publishing to brocker %s %s", topic_brocker, payload)
                self._brocker_client.publish(topic_brocker, payload=payload, retain=True)

            if topic_poolaccess is not None:
                # Publish data to poolaccess
                self._logger.info("Publishing to poolaccess %s %s", topic_poolaccess, payload)
                self._poolaccess_client.publish(topic_poolaccess, payload=payload)


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
        self._brocker_client.on_message = self.on_brocker_message
        self._brocker_client.on_disconnect = self.on_disconnect
        if self._brocker_client.establish_connection() != 0:
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
        # Instanciate entities
        for e in json.loads(content):
            if "disabled" in e and e["disabled"]:
                continue
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
    brocker_client = MqttClient(config["MQTT_HOST"], config["MQTT_PORT"],
                                config["MQTT_USER"] if "MQTT_USER" in config else None,
                                config["MQTT_PASSWORD"] if "MQTT_PASSWORD" in config else None)
    poolaccess_client = PoolAccessClient(config["DEVICE_TOKEN"])
    hass_entities = load_entities(os.path.join(os.path.dirname(__file__), "entities.json"), config)
    logger = logging.getLogger()
    logger.info("Starting Bridge")
    bridge = PoolAccessMqttBridge(
        config["MQTT_BASE_TOPIC"],
        config["DEVICE_SERIAL"],
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
