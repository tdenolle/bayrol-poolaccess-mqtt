import json
import os
import unittest
from unittest.mock import MagicMock, patch, ANY

from paho.mqtt.client import MQTTMessage, MQTT_ERR_SUCCESS, MQTT_ERR_AUTH, MQTT_ERR_CONN_REFUSED

from app.PoolAccessMqttBridge import PoolAccessMqttBridge, load_entities, main
from app.Translation import LanguageManager
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Climate import Climate
from app.hass.MessagesSensor import MessagesSensor
from app.hass.Sensor import Sensor
from app.hass.Switch import Switch
from app.mqtt.MqttClient import MqttClient
from app.mqtt.PoolAccessClient import PoolAccessClient, BAYROL_POOLACCESS_BASE_TOPIC


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

        self.device = BayrolPoolaccessDevice("24ASE2-45678")

        # Mock entities
        self.entities = [
            Sensor({"uid": "123", "key": "temperature", "name": "Température", }, self.device,
                   self.config["HASS_DISCOVERY_PREFIX"]),
            Climate({"uid_temp": "456", "uid_mode": "457", "key": "pac", "name": "PAC"}, self.device,
                    self.config["HASS_DISCOVERY_PREFIX"]),
            Switch({"uid": "789", "key": "ph_switch", "name": "Activate pH"}, self.device,
                   self.config["HASS_DISCOVERY_PREFIX"])
        ]

        # Mock MQTT clients
        self.poolaccess_client = MagicMock(spec=PoolAccessClient)
        self.broker_client = MagicMock(spec=MqttClient)

        # On configure le mock pour build_topic
        self.poolaccess_client.build_topic.side_effect = lambda mode, uid: "%s/%s/%s/%s" % (
        BAYROL_POOLACCESS_BASE_TOPIC, self.device.id, mode.value, uid)

        # Create instance of PoolAccessMqttBridge
        self.bridge = PoolAccessMqttBridge(
            self.config["MQTT_BASE_TOPIC"],
            self.config["DEVICE_SERIAL"],
            self.entities,
            self.poolaccess_client,
            self.broker_client
        )
        # avoid waiting for delay when reconnecting in connect loop
        self.bridge._reconnect_delay = 0

        # Init Singleton
        lang = LanguageManager()
        lang.setup("fr")

    def build_topic_mock(self, mode, id):
        return "%s/%s/%s/%s" % (BAYROL_POOLACCESS_BASE_TOPIC, self.device.id, mode.value, id)

    def test_init(self):
        self.assertEqual(self.bridge._poolaccess_device_serial, self.config["DEVICE_SERIAL"])
        self.assertEqual(self.bridge._mqtt_base_topic, self.config["MQTT_BASE_TOPIC"])
        self.assertEqual(self.bridge._hass_entities, self.entities)
        self.assertEqual(self.bridge._poolaccess_client, self.poolaccess_client)
        self.assertEqual(self.bridge._broker_client, self.broker_client)

    @patch('app.PoolAccessMqttBridge.PoolAccessMqttBridge._multi_loop')
    def test_start(self, mock_multi_loop):
        # Mock connect responses
        self.poolaccess_client.establish_connection.return_value = 0
        self.broker_client.establish_connection.return_value = 0

        # Call start
        self.bridge.start()

        # Assert connect calls
        self.poolaccess_client.establish_connection.assert_called_once()
        self.broker_client.establish_connection.assert_called_once()

        mock_multi_loop.assert_called_once()

    @patch('app.PoolAccessMqttBridge.PoolAccessMqttBridge._multi_loop')
    def test_start_with_connection_errors(self, mock_multi_loop):
        # Mock connect responses
        self.poolaccess_client.establish_connection.return_value = 1
        self.broker_client.establish_connection.return_value = 1

        # Call start
        self.bridge.start()

        # Assert connect calls
        self.poolaccess_client.establish_connection.assert_called_once()
        self.broker_client.establish_connection.assert_called_once()

        # Assert multi_loop not called
        mock_multi_loop.assert_not_called()

    def test_multi_loop_with_success(self):
        # Mock connect responses
        self.poolaccess_client.loop.return_value = MQTT_ERR_SUCCESS
        self.broker_client.loop.return_value = MQTT_ERR_SUCCESS

        self.bridge._multi_loop(loop=False)
        self.poolaccess_client.loop.assert_called_once()
        self.broker_client.loop.assert_called_once()

    def test_multi_loop_with_connection_errors(self):
        # Mock connect responses
        self.poolaccess_client.loop.return_value = MQTT_ERR_AUTH
        self.broker_client.loop.return_value = MQTT_ERR_CONN_REFUSED
        self.poolaccess_client.reconnect.side_effect = Exception('Poolaccess Test Exception')
        self.broker_client.reconnect.side_effect = Exception('Brocker Test Exception')

        self.bridge._multi_loop(loop=False)

        # loop calls
        self.poolaccess_client.loop.assert_called_once()
        self.broker_client.loop.assert_called_once()

        # reconnect calls
        self.poolaccess_client.reconnect.assert_called_once()
        self.broker_client.reconnect.assert_called_once()

    def test_on_poolaccess_message(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/24ASE2-45678/v/123"
        message.payload = b"{\"t\" : \"123\", \"v\" : \"255\"}"
        self.bridge.on_poolaccess_message(self.poolaccess_client, None, message)
        (self.broker_client.publish
         .assert_called_once_with("bayrol/sensor/24ASE2-45678/temperature", ANY, ANY, retain=True))
        # Check payload via args manually because of createdAt date value
        payload = str(self.broker_client.publish.call_args[0][1])
        self.assertIn("v", payload)
        self.assertIn("updatedAt", payload)

    def test_on_poolaccess_message_with_empty_payload(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/24ASE2-45678/v/123"
        message.payload = b""
        self.bridge.on_poolaccess_message(self.poolaccess_client, None, message)
        self.broker_client.publish.assert_called_once()

    def test_on_poolaccess_message_with_no_payload(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/24ASE2-45678/v/123"
        message.payload = None
        self.bridge.on_poolaccess_message(self.poolaccess_client, None, message)
        self.broker_client.publish.assert_not_called()

    def test_on_poolaccess_message_with_malformed_payload(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/24ASE2-45678/v/123"
        message.payload = b"{"
        self.bridge.on_poolaccess_message(self.poolaccess_client, None, message)
        self.broker_client.publish.assert_not_called()

    def test_on_broker_message_switch(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "bayrol/switch/24ASE2-45678/ph_switch/set"
        message.payload = b"{\"v\" : \"on\"}"
        self.bridge.on_broker_message(self.broker_client, None, message)
        self.broker_client.publish.assert_called_once_with("bayrol/switch/24ASE2-45678/ph_switch",
                                                           payload=b'{"v" : "on"}')
        self.poolaccess_client.publish.assert_called_once_with("d02/24ASE2-45678/s/789", payload=b'{"v" : "on"}')

    def test_on_broker_message_climate(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "bayrol/climate/24ASE2-45678/pac/temperature/set"
        message.payload = b"{\"v\" : \"123\"}"
        self.bridge.on_broker_message(self.broker_client, None, message)
        self.broker_client.publish.assert_called_once_with("bayrol/climate/24ASE2-45678/pac/temperature",
                                                           payload=b'{"v" : "123"}')
        self.poolaccess_client.publish.assert_called_once_with("d02/24ASE2-45678/s/456", payload=b'{"v" : "123"}')

    def test_on_broker_message_with_not_set(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "bayrol/switch/24ASE2-45678/ph_switch"
        message.payload = None
        self.bridge.on_broker_message(self.broker_client, None, message)
        self.poolaccess_client.publish.assert_not_called()

    def test_on_broker_message_with_no_command_set(self):
        message = MagicMock(spec=MQTTMessage)
        message.topic = "bayrol/switch/24ASE2-45678/ph_switch"
        message.payload = "{}"
        self.bridge.on_broker_message(self.broker_client, None, message)
        self.poolaccess_client.publish.assert_not_called()

    def test_on_poolaccess_connect(self):
        self.bridge.on_poolaccess_connect(self.poolaccess_client, None, None, 0, None)
        self.poolaccess_client.publish.assert_has_calls([
            unittest.mock.call("d02/24ASE2-45678/g/123"),
            unittest.mock.call("d02/24ASE2-45678/g/456"),
            unittest.mock.call("d02/24ASE2-45678/g/457"),
            unittest.mock.call("d02/24ASE2-45678/g/789")
        ], any_order=True)
        self.broker_client.publish.assert_has_calls([
            unittest.mock.call('bayrol/sensor/24ASE2-45678/temperature/config', payload=json.dumps({
                "name": "Température",
                "unique_id": "bayrol_24ase245678_temperature",
                "object_id": "bayrol_24ase245678_temperature",
                "state_topic": "bayrol/sensor/24ASE2-45678/temperature",
                "availability": [{"topic": "bayrol/sensor/24ASE2-45678/status",
                                  "value_template": "{{ \'online\' if value_json.v | float > 17.0 else \'offline\' }}"}],
                "value_template": "{{ value_json.v }}",
                "device": self.device
            }), retain=True),
            unittest.mock.call('bayrol/climate/24ASE2-45678/pac/config', payload=json.dumps({
                "name": "PAC",
                "unique_id": "bayrol_24ase245678_pac",
                "object_id": "bayrol_24ase245678_pac",
                "state_topic": "bayrol/climate/24ASE2-45678/pac",
                "availability": [{"topic": "bayrol/sensor/24ASE2-45678/status",
                                  "value_template": "{{ \'online\' if value_json.v | float > 17.0 else \'offline\' }}"}],
                "value_template": "{{ value_json.v }}",
                "temperature_command_topic": "bayrol/climate/24ASE2-45678/pac/temperature/set",
                "mode_command_topic": "bayrol/climate/24ASE2-45678/pac/mode/set",
                "temperature_state_topic": "bayrol/climate/24ASE2-45678/pac/temperature",
                "mode_state_topic": "bayrol/climate/24ASE2-45678/pac/mode",
                "device": self.device
            }), retain=True),
            unittest.mock.call('bayrol/switch/24ASE2-45678/ph_switch/config', payload=json.dumps({
                "name": "Activate pH",
                "unique_id": "bayrol_24ase245678_ph_switch",
                "object_id": "bayrol_24ase245678_ph_switch",
                "state_topic": "bayrol/switch/24ASE2-45678/ph_switch",
                "availability": [{
                    "topic": "bayrol/sensor/24ASE2-45678/status",
                    "value_template": "{{ 'online' if value_json.v | float > 17.0 else 'offline' }}"
                }],
                "value_template": "{{ value_json.v }}",
                "payload_on": "on",
                "payload_off": "off",
                "command_topic": "bayrol/switch/24ASE2-45678/ph_switch/set",
                "device": self.device
            }), retain=True)

        ])
        self.poolaccess_client.subscribe.assert_called_once_with("d02/24ASE2-45678/v/#")

    def test_on_broker_connect(self):
        self.bridge.on_broker_connect(self.broker_client, None, None, 0, None)

    def test_on_broker_connect_failed(self):
        with self.assertRaises(SystemExit) as se:
            self.bridge.on_broker_connect(self.broker_client, None, None, 1, None)
        e = se.exception
        self.assertEqual(e.code, 1)

    def test_on_poolaccess_connect_failed(self):
        with self.assertRaises(SystemExit) as se:
            self.bridge.on_poolaccess_connect(self.poolaccess_client, None, None, 1, None)
        e = se.exception
        self.assertEqual(e.code, 1)

    def test_on_poolaccess_disconnect(self):
        c = PoolAccessClient("__token__", "__serial__")
        c.on_disconnect = self.bridge.on_disconnect
        c._do_on_disconnect(False, None)
        assert self.bridge.on_disconnect

    def test_load_entities_without_serial(self):
        with self.assertRaises(KeyError) as ke:
            load_entities("/tmp/fake.json", {"XXX": "YYY"})
            self.assertEqual(ke.msg, "DEVICE_SERIAL option can not be found in configuration.")

    def test_load_entities(self):
        # Mock entities.json file
        entities_json_path = os.path.join(os.path.dirname(__file__), "entities.json")
        with open(entities_json_path, 'w') as f:
            json.dump([
                {"uid": "1", "key": "temperature", "unit_of_measurement": "°C", "attr_dyn": "#XXX/#DEVICE_SERIAL/on"},
                {"uid": "10", "key": "messages", "__class__": "MessagesSensor"},
                {"uid": "15", "key": "se_on_off", "__class__": "Switch", "filters": {"DEVICE_SERIAL": "1.0"}},
                {"uid": "16", "key": "ph_on_off", "__class__": "Sensor", "disable": True},
                {"uid": "17", "key": "en_filtered", "__class__": "Climate", "filters": {"XXX": "ZZZ"}},
            ], f)

        # Load entities
        entities = load_entities(entities_json_path, {"DEVICE_SERIAL": "1.0", "XXX": "YYY"})

        # Assert sensor types
        self.assertEqual(len(entities), 3)
        self.assertIsInstance(entities[0], Sensor)
        self.assertEqual(entities[0].get_attr("attr_dyn"), "YYY/1.0/on")

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
