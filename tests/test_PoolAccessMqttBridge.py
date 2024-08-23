import os
import unittest
from unittest.mock import MagicMock, patch, ANY, Mock
import json

from paho.mqtt.client import MQTTMessage, MQTT_ERR_SUCCESS, MQTT_ERR_AUTH, MQTT_ERR_CONN_REFUSED

from app.PoolAccessMqttBridge import PoolAccessMqttBridge, Sensor, load_entities, main
from app.hass.MessagesSensor import MessagesSensor
from app.hass.Switch import Switch
from app.mqtt.MqttClient import MqttClient
from app.mqtt.PoolAccessClient import PoolAccessClient


class TestPoolAccessMqttBridge(unittest.TestCase):

    def setUp(self):
        # Mock configuration
        self.config = {
            "MQTT_HOST": "mqtt.example.com",
            "MQTT_PORT": 1883,
            "MQTT_USER": "user",
            "MQTT_PASSWORD": "password",
            "DEVICE_TOKEN": "token",
            "DEVICE_SERIAL": "24ASE2-45678",
            "MQTT_BASE_TOPIC": "homeassistant",
            "HASS_DISCOVERY_PREFIX": "bayrol",
            "LOG_LEVEL": "INFO"
        }

        # Mock entities
        self.entities = [
            Sensor({"uid": "123", "key": "temperature", "name": "Température", }),
            Sensor({"uid": "456", "key": "ph", "name": "pH"}),
            Switch({"uid": "789", "key": "ph_switch", "name": "Activate pH"})
        ]

        # Mock MQTT clients
        self.poolaccess_client = MagicMock(spec=PoolAccessClient)
        self.brocker_client = MagicMock(spec=MqttClient)

        # Create instance of PoolAccessMqttBridge
        self.bridge = PoolAccessMqttBridge(
            self.config["MQTT_BASE_TOPIC"],
            self.config["DEVICE_SERIAL"],
            self.config["HASS_DISCOVERY_PREFIX"],
            self.entities,
            self.poolaccess_client,
            self.brocker_client
        )
        # avoid waiting for delay when reconnecting in connect loop
        self.bridge._reconnect_delay = 0

    def test_init(self):
        self.assertEqual(self.bridge._poolaccess_device_serial, self.config["DEVICE_SERIAL"])
        self.assertEqual(self.bridge._mqtt_base_topic, self.config["MQTT_BASE_TOPIC"])
        self.assertEqual(self.bridge._hass_discovery_prefix, self.config["HASS_DISCOVERY_PREFIX"])
        self.assertEqual(self.bridge._hass_entities, self.entities)
        self.assertEqual(self.bridge._poolaccess_client, self.poolaccess_client)
        self.assertEqual(self.bridge._brocker_client, self.brocker_client)

    @patch('app.PoolAccessMqttBridge.PoolAccessMqttBridge._multi_loop')
    def test_start(self, mock_multi_loop):
        # Mock connect responses
        self.poolaccess_client.establish_connection.return_value = 0
        self.brocker_client.establish_connection.return_value = 0

        # Call start
        self.bridge.start()

        # Assert connect calls
        self.poolaccess_client.establish_connection.assert_called_once()
        self.brocker_client.establish_connection.assert_called_once()

        mock_multi_loop.assert_called_once()

    @patch('app.PoolAccessMqttBridge.PoolAccessMqttBridge._multi_loop')
    def test_start_with_connection_errors(self, mock_multi_loop):
        # Mock connect responses
        self.poolaccess_client.establish_connection.return_value = 1
        self.brocker_client.establish_connection.return_value = 1

        # Call start
        self.bridge.start()

        # Assert connect calls
        self.poolaccess_client.establish_connection.assert_called_once()
        self.brocker_client.establish_connection.assert_called_once()

        # Assert multi_loop not called
        mock_multi_loop.assert_not_called()

    def test_multi_loop_with_success(self):
        # Mock connect responses
        self.poolaccess_client.loop.return_value = MQTT_ERR_SUCCESS
        self.brocker_client.loop.return_value = MQTT_ERR_SUCCESS

        self.bridge._multi_loop(loop=False)
        self.poolaccess_client.loop.assert_called_once()
        self.brocker_client.loop.assert_called_once()

    def test_multi_loop_with_connection_errors(self):
        # Mock connect responses
        self.poolaccess_client.loop.return_value = MQTT_ERR_AUTH
        self.brocker_client.loop.return_value = MQTT_ERR_CONN_REFUSED
        self.poolaccess_client.reconnect.side_effect = Exception('Poolaccess Test Exception')
        self.brocker_client.reconnect.side_effect = Exception('Brocker Test Exception')

        self.bridge._multi_loop(loop=False)

        # loop calls
        self.poolaccess_client.loop.assert_called_once()
        self.brocker_client.loop.assert_called_once()

        # reconnect calls
        self.poolaccess_client.reconnect.assert_called_once()
        self.brocker_client.reconnect.assert_called_once()

    def test_on_poolaccess_message(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/24ASE2-45678/v/123"
        message.payload = b"{\"v\" : \"255\"}"
        self.bridge.on_poolaccess_message(self.poolaccess_client, None, message)
        (self.brocker_client.publish
         .assert_called_once_with("bayrol/sensor/24ASE2-45678/temperature", ANY, message.qos, retain=True))
        # Check payload via args manually because of createdAt date value
        payload = str(self.brocker_client.publish.call_args[0][1])
        self.assertIn("v", payload)
        self.assertIn("updatedAt", payload)


    def test_on_brocker_message(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "bayrol/switch/24ASE2-45678/ph_switch/set"
        message.payload = b"{\"v\" : \"on\"}"
        self.bridge.on_brocker_message(self.brocker_client, None, message)
        (self.poolaccess_client.publish
         .assert_called_once_with("d02/24ASE2-45678/s/789", qos=0, payload=b'{"v" : "on"}', retain=False))

    def test_on_brocker_message_with_not_set(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "bayrol/switch/24ASE2-45678/ph_switch"
        self.bridge.on_brocker_message(self.brocker_client, None, message)
        self.poolaccess_client.publish.assert_not_called()

    def test_on_poolaccess_connect(self):
        self.bridge.on_poolaccess_connect(None, None, None, 0, None)
        self.poolaccess_client.publish.assert_has_calls([
            unittest.mock.call("d02/24ASE2-45678/g/123", qos=0, payload=None),
            unittest.mock.call("d02/24ASE2-45678/g/456", qos=0, payload=None)
        ])
        self.brocker_client.publish.assert_has_calls([
            unittest.mock.call('bayrol/sensor/24ASE2-45678/temperature/config', qos=1, payload=json.dumps({
                "unique_id": "bayrol_24ase245678_temperature",
                "name": "Température",
                "state_topic": "bayrol/sensor/24ASE2-45678/temperature",
                "availability": [{"topic": "bayrol/sensor/24ASE2-45678/status",
                                  "value_template": "{{ \'online\' if value_json.v | float > 17.0 else \'offline\' }}"}],
                "value_template": "{{ value_json.v }}",
                "device": {
                    "identifiers": ["24ASE2-45678"],
                    "manufacturer": "Bayrol",
                    "model": "Automatic Salt",
                    "name": "Bayrol 24ASE2-45678"
                }
            }), retain=True),
            unittest.mock.call('bayrol/sensor/24ASE2-45678/ph/config', qos=1, payload=json.dumps({
                "unique_id": "bayrol_24ase245678_ph",
                "name": "pH",
                "state_topic": "bayrol/sensor/24ASE2-45678/ph",
                "availability": [{"topic": "bayrol/sensor/24ASE2-45678/status",
                                  "value_template": "{{ \'online\' if value_json.v | float > 17.0 else \'offline\' }}"}],
                "value_template": "{{ value_json.v }}",
                "device": {
                    "identifiers": ["24ASE2-45678"],
                    "manufacturer": "Bayrol",
                    "model": "Automatic Salt",
                    "name": "Bayrol 24ASE2-45678"
                }
            }), retain=True)
        ])
        self.poolaccess_client.subscribe.assert_called_once_with("d02/24ASE2-45678/v/#", qos=1)

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

    def test_on_poolaccess_disconnect(self):
        c = PoolAccessClient("__token__")
        c.on_disconnect = self.bridge.on_disconnect
        c._do_on_disconnect(False, None)
        assert self.bridge.on_disconnect

    def test_load_sensors(self):
        # Mock entities.json file
        entities_json_path = os.path.join(os.path.dirname(__file__), "entities.json")
        with open(entities_json_path, 'w') as f:
            json.dump([
                {"uid": "1", "key": "temperature", "unit_of_measurement": "°C"},
                {"uid": "10", "key": "messages", "__class__": "MessagesSensor"},
                {"uid": "15", "key": "sw", "__class__": "Switch"}
            ], f)

        # Load entities
        entities = load_entities(entities_json_path)

        # Assert sensor types
        self.assertIsInstance(entities[0], Sensor)
        self.assertIsInstance(entities[1], MessagesSensor)
        self.assertIsInstance(entities[2], Switch)

        # Clean up
        os.remove(entities_json_path)

    @patch('app.PoolAccessMqttBridge.PoolAccessMqttBridge.start')
    def test_main(self, mock_start):
        main(self.config)
        mock_start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
