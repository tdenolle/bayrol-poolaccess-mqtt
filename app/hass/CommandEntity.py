#!/usr/bin/env python3
from paho.mqtt.client import MQTTMessage
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity
from app.mqtt import MqttClient, PoolAccessClient
from app.mqtt.PoolAccessClient import PoolAccessTopicMode


class CommandEntity(Entity):
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, discovery_prefix: str = "homeassistant"):
        super().__init__(data, device, discovery_prefix)
        data["payload_on"] = "on"
        data["payload_off"] = "off"
        if "command_topic" not in data:
            data["command_topic"] = "%s/set" % data["state_topic"]

    @property
    def type(self) -> str:
        raise NotImplementedError("CommandEntity type not implemented")

    @property
    def command_topic(self) -> str:
        return self._attributes["command_topic"]

    def on_broker_connect(self, client: MqttClient):
        # Subscribing to Command Topic
        self._logger.info("Subscribing to topic: %s", self.command_topic)
        client.subscribe(self.command_topic)

    def on_broker_message(self, client: PoolAccessClient, broker: MqttClient, message: MQTTMessage):
        if message.topic == self.command_topic:
            # Publish data to broker to persist it
            self._logger.info("Publishing to broker %s %s", self.state_topic, str(message.payload))
            broker.publish(self.state_topic, payload=message.payload)
            # Publish data to poolaccess
            poolaccess_topic = client.build_topic(PoolAccessTopicMode.SET, self.uid)
            self._logger.info("Publishing to poolaccess %s %s", poolaccess_topic, message.payload)
            client.publish(poolaccess_topic, payload=message.payload)
