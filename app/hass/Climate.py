#!/usr/bin/env python3
from json import JSONDecodeError

from paho.mqtt.client import MQTTMessage

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity, load_attr
from app.mqtt import PoolAccessClient, MqttClient
from app.mqtt.PoolAccessClient import PoolAccessTopicMode


class Climate(Entity):
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, discovery_prefix: str = "homeassistant"):
        super().__init__(data, device, discovery_prefix)

        self._uid_mode = load_attr("uid_mode", data)
        self._uid_temp = load_attr("uid_temp", data)

        if "temperature_command_topic" not in data:
            data["temperature_command_topic"] = "%s/temperature/set" % data["state_topic"]

        if "mode_command_topic" not in data:
            data["mode_command_topic"] = "%s/mode/set" % data["state_topic"]

        if "temperature_state_topic" not in data:
            data["temperature_state_topic"] = "%s/temperature" % data["state_topic"]

        if "mode_state_topic" not in data:
            data["mode_state_topic"] = "%s/mode" % data["state_topic"]

    @property
    def type(self) -> str:
        return "climate"

    @property
    def uid_mode(self) -> str:
        return self._uid_mode

    @property
    def uid_temp(self) -> str:
        return self._uid_temp

    @property
    def temperature_command_topic(self) -> str:
        return self._attributes["temperature_command_topic"]

    @property
    def mode_command_topic(self) -> str:
        return self._attributes["mode_command_topic"]

    @property
    def temperature_state_topic(self) -> str:
        return self._attributes["temperature_state_topic"]

    @property
    def mode_state_topic(self) -> str:
        return self._attributes["mode_state_topic"]

    def build_config(self):
        return super().build_config()

    def on_poolaccess_connect(self, client: PoolAccessClient):
        for uid in [self.uid_mode, self.uid_temp]:
            topic = client.build_topic(PoolAccessTopicMode.GET, uid)
            self._logger.info("Publishing to poolaccess : %s", topic)
            client.publish(topic)

    def on_broker_connect(self, broker: MqttClient):
        # Subscribing to Temperature & Mode Topics
        for topic in [self.temperature_command_topic, self.mode_command_topic]:
            self._logger.info("Subscribing to broker : %s", topic)
            broker.subscribe(topic)

    def on_poolaccess_message(self, client: PoolAccessClient, broker: MqttClient, message: MQTTMessage):
        if message.topic == client.build_topic(PoolAccessTopicMode.VALUE, self.uid_temp) :
            self._process_poolaccess_message(message, broker, self.temperature_state_topic)

        if message.topic == client.build_topic(PoolAccessTopicMode.VALUE, self.uid_mode) :
            self._process_poolaccess_message(message, broker, self.mode_state_topic)

    def _process_poolaccess_message(self, message: MQTTMessage, broker: MqttClient, topic):
        self._logger.info("Reading %s %s", message.topic, str(message.payload))
        try:
            payload = self.get_payload(message.payload)
            broker.publish(topic, payload, message.qos, retain=True)
            self._logger.info("Publishing to broker %s %s", topic, str(payload))
        except JSONDecodeError as jde:
            self._logger.error(jde)

    def on_broker_message(self, client: PoolAccessClient, broker: MqttClient, message: MQTTMessage):
        if message.topic == self.temperature_command_topic:
            self._logger.info("Reading %s %s", message.topic, str(message.payload))
            self._process_broker_message(client, broker, self.uid_temp, self.temperature_command_topic, message.payload)

        if message.topic == self.mode_command_topic:
            self._logger.info("Reading %s %s", message.topic, str(message.payload))
            self._process_broker_message(client, broker, self.uid_mode, self.mode_command_topic, message.payload)

    def _process_broker_message(self, client: PoolAccessClient, broker: MqttClient, uid, state_topic:str, payload):
        # Publish data to broker to persist it
        self._logger.info("Publishing to broker %s %s", self.state_topic, payload)
        broker.publish(state_topic, payload=payload, retain=True)
        # Publish data to poolaccess
        poolaccess_topic = client.build_topic(PoolAccessTopicMode.SET, uid)
        self._logger.info("Publishing to poolaccess %s %s", poolaccess_topic, payload)
        client.publish(poolaccess_topic, payload=payload)