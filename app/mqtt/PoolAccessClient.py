from .MqttClient import MqttClient

BAYROL_POOLACCESS_MQTT_TRANSPORT = "websockets"
BAYROL_POOLACCESS_MQTT_HOST = "www.bayrol-poolaccess.de"
BAYROL_POOLACCESS_MQTT_PORT = 8083
BAYROL_POOLACCESS_MQTT_PASSWORD = "*"


class PoolAccessClient(MqttClient):
    def __init__(self, token: str):
        super().__init__(BAYROL_POOLACCESS_MQTT_HOST, BAYROL_POOLACCESS_MQTT_PORT, token,
                         BAYROL_POOLACCESS_MQTT_PASSWORD, transport=BAYROL_POOLACCESS_MQTT_TRANSPORT)
        self.tls_set()
