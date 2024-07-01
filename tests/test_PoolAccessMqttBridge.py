import unittest
from unittest.mock import MagicMock, patch
import json

from paho.mqtt.client import MQTTMessage

from bayrol_poolaccess_mqtt.PoolAccessMqttBridge import PoolAccessMqttBridge, Sensor
from bayrol_poolaccess_mqtt.mqtt.MqttClient import MqttClient
from bayrol_poolaccess_mqtt.mqtt.PoolAccessClient import PoolAccessClient


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
            Sensor({"uid": "123", "key": "temperature", "name": "Température", }),
            Sensor({"uid": "456", "key": "ph", "name": "pH"})
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
        self.poolaccess_client.establish_connection.assert_called_once()
        self.brocker_client.establish_connection.assert_called_once()
        mock_multi_loop.assert_called_once()

    def test_on_poolaccess_message(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/AS12345678/v/123"
        message.payload = b"{v : '255'}"
        self.bridge.on_poolaccess_message(self.poolaccess_client, None, message)
        self.brocker_client.publish.assert_called_once_with("bayrol/sensor/AS12345678/temperature", b"{v : '255'}",
                                                            message.qos, retain=True)

    def test_on_poolaccess_connect(self):
        self.bridge.on_poolaccess_connect(None, None, None, 0, None)
        self.poolaccess_client.publish.assert_has_calls([
            unittest.mock.call("d02/AS12345678/g/123", qos=0, payload=None),
            unittest.mock.call("d02/AS12345678/g/456", qos=0, payload=None)
        ])
        self.brocker_client.publish.assert_has_calls([
            unittest.mock.call('bayrol/sensor/AS12345678/temperature/config', qos=1, payload=json.dumps({
                "unique_id": "bayrol_as12345678_temperature",
                "name": "Température",
                "state_topic": "bayrol/sensor/AS12345678/temperature",
                "availability": [{"topic": "bayrol/sensor/AS12345678/status",
                                  "value_template": "{{ \'online\' if value_json.v | float > 17.0 else \'offline\' }}"}],
                "value_template": "{{ value_json.v }}",
                "device": {
                    "identifiers": ["AS12345678"],
                    "manufacturer": "Bayrol",
                    "model": "Automatic Salt",
                    "name": "Bayrol AS12345678"
                },
                "json_attributes_topic": "bayrol/sensor/AS12345678/temperature"
            }), retain=True),
            unittest.mock.call('bayrol/sensor/AS12345678/ph/config', qos=1, payload=json.dumps({
                "unique_id": "bayrol_as12345678_ph",
                "name": "pH",
                "state_topic": "bayrol/sensor/AS12345678/ph",
                "availability": [{"topic": "bayrol/sensor/AS12345678/status",
                                  "value_template": "{{ \'online\' if value_json.v | float > 17.0 else \'offline\' }}"}],
                "value_template": "{{ value_json.v }}",
                "device": {
                    "identifiers": ["AS12345678"],
                    "manufacturer": "Bayrol",
                    "model": "Automatic Salt",
                    "name": "Bayrol AS12345678"
                },
                "json_attributes_topic": "bayrol/sensor/AS12345678/ph"
            }), retain=True)
        ])
        self.poolaccess_client.subscribe.assert_called_once_with("d02/AS12345678/v/#", qos=1)

    def test_on_brocker_connect(self):
        self.bridge.on_brocker_connect(self.brocker_client, None, None, 0, None)

    def test_on_brocker_connect_failed(self):
        with self.assertRaises(SystemExit) as se:
            self.bridge.on_brocker_connect(self.brocker_client, None, None, 1, None)
        e = se.exception
        self.assertEqual(e.code, 1)

    def test_on_poolaccess_connect_failed(self):
        with self.assertRaises(SystemExit) as se:
            self.bridge.on_poolaccess_connect(self.poolaccess_client, None, None, 1, None)
        e = se.exception
        self.assertEqual(e.code, 1)

if __name__ == '__main__':
    unittest.main()
