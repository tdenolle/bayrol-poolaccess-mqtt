from random import random

import paho.mqtt.client as mqtt

DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_KEEPALIVE = 60
DEFAULT_RECONNECT_DELAY = 60


class MqttClient(mqtt.Client):
    def __init__(self, host: str, port: int, user: str, password: str, transport: str = "tcp"):
        self._client_id = '_'.join(['user', str(random().hex())[4:12]])
        self._transport = transport
        super().__init__(client_id=self._client_id,
                         clean_session=False,
                         transport=self._transport)
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        if self._user is not None:
            self.username_pw_set(
                self._user,
                self._password)

    def establish_connection(self):
        h = self._host
        super().connect(self._host, self._port)
