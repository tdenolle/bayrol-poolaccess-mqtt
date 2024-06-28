import unittest
from unittest.mock import MagicMock, patch
import json
from ..app.PoolAccessMqttBridge import PoolAccessMqttBridge, Sensor
from ..app.mqtt.MqttClient import MqttClient
from ..app.mqtt.PoolAccessClient import PoolAccessClient


class TestPoolAccessMqttBridge(unittest.TestCase):

    def setUp(self):
        # Mock configuration
        self.config = {
            "MQTT_HOST": "mqtt.example.com",
            "MQTT_PORT": 1883,
            "MQTT_USER": "user",
            "MQTT_PASSWORD": "password",
            "DEVICE_TOKEN": "token",
            "DEVICE_SERIAL": "AS12345678",
            "MQTT_BASE_TOPIC": "homeassistant",
            "HASS_DISCOVERY_PREFIX": "bayrol",
            "LOG_LEVEL": "INFO"
        }

        # Mock sensors
        self.sensors = [
            Sensor("temperature", "temperature", "°C", "d02/AS12345678/g/temperature", "temperature", None),
            Sensor("ph", "ph", "", "d02/AS12345678/g/ph", "ph", None)
        ]

        # Mock MQTT clients
        self.poolaccess_client = MagicMock(spec=PoolAccessClient)
        self.brocker_client = MagicMock(spec=MqttClient)

        # Create instance of PoolAccessMqttBridge
        self.bridge = PoolAccessMqttBridge(
            self.config["MQTT_BASE_TOPIC"],
            self.config["DEVICE_SERIAL"],
            self.config["HASS_DISCOVERY_PREFIX"],
            self.sensors,
            self.poolaccess_client,
            self.brocker_client
        )

    def test_init(self):
        self.assertEqual(self.bridge._poolaccess_device_serial, self.config["DEVICE_SERIAL"])
        self.assertEqual(self.bridge._mqtt_base_topic, self.config["MQTT_BASE_TOPIC"])
        self.assertEqual(self.bridge._hass_discovery_prefix, self.config["HASS_DISCOVERY_PREFIX"])
        self.assertEqual(self.bridge._base_sensor_topic, "bayrol/sensor/AS12345678")
        self.assertEqual(self.bridge._hass_sensors, self.sensors)
        self.assertEqual(self.bridge._poolaccess_client, self.poolaccess_client)
        self.assertEqual(self.bridge._brocker_client, self.brocker_client)

    @patch('bayrol_poolaccess_mqtt.PoolAccessMqttBridge.PoolAccessMqttBridge._multi_loop')
    def test_start(self, mock_multi_loop):
        self.bridge.start()
        self.poolaccess_client.on_message.assert_called_once_with(self.bridge.on_poolaccess_message)
        self.poolaccess_client.on_connect.assert_called_once_with(self.bridge.on_poolaccess_connect)
        self.poolaccess_client.establish_connection.assert_called_once()
        self.brocker_client.on_connect.assert_called_once_with(self.bridge.on_brocker_connect)
        self.brocker_client.establish_connection.assert_called_once()
        mock_multi_loop.assert_called_once()

    def test_on_poolaccess_message(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/AS12345678/v/temperature"
        message.payload = b"25.5"
        self.bridge.on_poolaccess_message(None, None, message)
        self.brocker_client.publish.assert_called_once_with("bayrol/sensor/AS12345678/temperature", b"25.5",
                                                            message.qos, retain=True)

    def test_on_poolaccess_connect(self):
        self.bridge.on_poolaccess_connect(None, None, None, 0)
        self.poolaccess_client.publish.assert_has_calls([
            unittest.mock.call("d02/AS12345678/g/temperature", qos=0, payload=None),
            unittest.mock.call("d02/AS12345678/g/ph", qos=0, payload=None)
        ])
        self.brocker_client.publish.assert_has_calls([
            unittest.mock.call('bayrol/sensor/AS12345678/temperature/config', json.dumps({
                "device_class": "temperature",
                "name": "Bayrol AS12345678 Temperature",
                "state_topic": "bayrol/sensor/AS12345678/temperature",
                "unit_of_measurement": "°C",
                "value_template": "{{ value }}",
                "unique_id": "bayrol_AS12345678_temperature",
                "device": {
                    "identifiers": ["AS12345678"],
                    "manufacturer": "Bayrol",
                    "model": "Automatic Salt",
                    "name": "Bayrol AS12345678"
                }
            }), qos=1, retain=True),
            unittest.mock.call('bayrol/sensor/AS12345678/ph/config', json.dumps({
                "device_class": "ph",
                "name": "Bayrol AS12345678 PH",
                "state_topic": "bayrol/sensor/AS12345678/ph",
                "unit_of_measurement": "",
                "value_template": "{{ value }}",
                "unique_id": "bayrol_AS12345678_ph",
                "device": {
                    "identifiers": ["AS12345678"],
                    "manufacturer": "Bayrol",
                    "model": "Automatic Salt",
                    "name": "Bayrol AS12345678"
                }
            }), qos=1, retain=True)
        ])
        self.poolaccess_client.subscribe.assert_called_once_with("d02/AS12345678/v/#", qos=1)

    def test_on_brocker_connect(self):
        self.bridge.on_brocker_connect(None, None, None, 0)

    def test_on_brocker_connect_failed(self):
        self.bridge.on_brocker_connect(None, None, None, 1)

    def test_on_poolaccess_connect_failed(self):
        self.bridge.on_poolaccess_connect(None, None, None, 1)


if __name__ == '__main__':
    unittest.main()
