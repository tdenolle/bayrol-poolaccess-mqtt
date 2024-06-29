from random import random

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

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
        if self._user is not None:
            self.username_pw_set(
                self._user,
                self._pwd)

    def establish_connection(self):
        super().connect(self._host, self._port)
