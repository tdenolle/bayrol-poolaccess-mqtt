#!/usr/bin/env python3
import logging
from random import random

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion, MQTTErrorCode

DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_KEEPALIVE = 60
DEFAULT_RECONNECT_DELAY = 60


class MqttClient(mqtt.Client):
    def __init__(self, host: str, port: int, user: str, password: str, transport: str = "tcp"):
        self._cid = '_'.join(['user', str(random().hex())[4:12]])
        self._transport = transport
        super().__init__(CallbackAPIVersion.VERSION2,
                         client_id=self._cid,
                         clean_session=False,
                         transport=self._transport)
        self._host = host
        self._port = port
        self._user = user
        self._pwd = password
        self._logger = logging.getLogger(__name__)
        if self._user is not None:
            self.username_pw_set(
                self._user,
                self._pwd)

    def establish_connection(self) -> MQTTErrorCode:
        try:
            return super().connect(self._host, self._port)
        except ConnectionRefusedError as e:
            if self._logger is not None:
                self._logger.error("Failed to connect to %s:%s. %s", self._host, self._port, e)
            return MQTTErrorCode.MQTT_ERR_CONN_REFUSED

