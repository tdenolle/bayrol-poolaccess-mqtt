#!/usr/bin/env python3
from enum import Enum

from .MqttClient import MqttClient


BAYROL_POOLACCESS_MQTT_TRANSPORT = "websockets"
BAYROL_POOLACCESS_MQTT_HOST = "www.bayrol-poolaccess.de"
BAYROL_POOLACCESS_MQTT_PORT = 8083
BAYROL_POOLACCESS_MQTT_PASSWORD = "*"
BAYROL_POOLACCESS_BASE_TOPIC = "d02"

class PoolAccessTopicMode(Enum):
    GET = "g"
    SET = "s"
    VALUE = "v"

class PoolAccessClient(MqttClient):
    def __init__(self, token: str, serial: str):
        super().__init__(BAYROL_POOLACCESS_MQTT_HOST, BAYROL_POOLACCESS_MQTT_PORT, token,
                         BAYROL_POOLACCESS_MQTT_PASSWORD, transport=BAYROL_POOLACCESS_MQTT_TRANSPORT)
        self._serial = serial
        self.tls_set()

    def build_topic(self, mode: PoolAccessTopicMode, uid):
        return "%s/%s/%s/%s" % (BAYROL_POOLACCESS_BASE_TOPIC, self._serial, mode.value, uid)
