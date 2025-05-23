import unittest
from unittest.mock import MagicMock
from app.hass.Climate import Climate
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.mqtt.PoolAccessClient import BAYROL_POOLACCESS_BASE_TOPIC


class TestClimate(unittest.TestCase):
    def setUp(self):
        self.device = BayrolPoolaccessDevice("24ASE2-45678")
        self.data = {
            "uid_temp": "456",
            "uid_mode": "457",
            "key": "pac",
            "name": "PAC"
        }
        self.discovery_prefix = "bayrol"
        self.climate = Climate(self.data, self.device, self.discovery_prefix)

    def test_init(self):
        self.assertEqual(self.climate.key, "pac")
        self.assertEqual(self.climate.name, "PAC")

    def test_build_config(self):
        topic, config = self.climate.build_config()
        self.assertIn("name", config)
        self.assertIn("unique_id", config)
        self.assertIn("state_topic", config)
        self.assertTrue(topic.endswith("/config"))

    def test_on_poolaccess_message_with_invalid_payload(self):
        # Mocking the PoolAccessClient and BrokerClient
        poolaccess_client = MagicMock()
        broker_client = MagicMock()
        message = MagicMock()

        # Mocking invalid payload
        message.topic = "d02/24ASE2-45678/v/456"
        message.payload = b'{'
        self.climate.on_poolaccess_message(poolaccess_client, broker_client, message)
        broker_client.publish.assert_not_called()

    def test_on_poolaccess_message(self):
        # Mocking the PoolAccessClient and BrokerClient
        poolaccess_client = MagicMock()
        # build_topic mocked to return a specific topic
        poolaccess_client.build_topic.side_effect = lambda mode, uid: "%s/%s/%s/%s" % (
        BAYROL_POOLACCESS_BASE_TOPIC, self.device.id, mode.value, uid)
        broker_client = MagicMock()
        message = MagicMock()

        # Mocking temperature message topic and payload
        message.topic = "d02/24ASE2-45678/v/456"
        message.payload = b'{"t": "456", "v": "22"}'
        self.climate.on_poolaccess_message(poolaccess_client, broker_client, message)
        broker_client.publish.assert_called()

        # Mocking mode message topic and payload
        message.topic = "d02/24ASE2-45678/v/457"
        message.payload = b'{"t": "457", "v": "auto"}'
        self.climate.on_poolaccess_message(poolaccess_client, broker_client, message)
        broker_client.publish.assert_called()

    def test_on_broker_message(self):
        poolaccess_client = MagicMock()
        broker_client = MagicMock()
        message = MagicMock()

        # Mocking temperature message topic and payload
        message.topic = "bayrol/climate/24ASE2-45678/pac/temperature/set"
        message.payload = b'{"v": "25"}'
        self.climate.on_broker_message(poolaccess_client, broker_client, message)
        poolaccess_client.publish.assert_called()
        broker_client.publish.assert_called()

        # Mocking mode message topic and payload
        message.topic = "bayrol/climate/24ASE2-45678/pac/mode/set"
        message.payload = b'{"v": "auto"}'
        self.climate.on_broker_message(poolaccess_client, broker_client, message)
        poolaccess_client.publish.assert_called()
        broker_client.publish.assert_called()

if __name__ == '__main__':
    unittest.main()