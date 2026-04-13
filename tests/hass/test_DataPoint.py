import json
import unittest
from unittest.mock import MagicMock

from paho.mqtt.client import MQTTMessage

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.DataPoint import DataPoint
from app.mqtt.PoolAccessClient import PoolAccessClient, BAYROL_POOLACCESS_BASE_TOPIC, PoolAccessTopicMode


class TestDataPoint(unittest.TestCase):
    def setUp(self):
        self.device = BayrolPoolaccessDevice("24ASE2-45678")

    def test_datapoint_creation(self):
        dp = DataPoint({"uid": "1.0", "key": "internal_temp"}, self.device)
        self.assertEqual(dp.uid, "1.0")
        self.assertEqual(dp.key, "internal_temp")
        self.assertFalse(dp.disable)
        self.assertIsNone(dp.value)

    def test_datapoint_without_uid(self):
        dp = DataPoint({"key": "internal_temp"}, self.device)
        self.assertIsNone(dp.uid)
        self.assertEqual(dp.key, "internal_temp")

    def test_key_value_error(self):
        dp = object.__new__(DataPoint)
        dp._key = None
        with self.assertRaises(ValueError):
            _ = dp.key

    def test_disable_value_error(self):
        dp = object.__new__(DataPoint)
        dp._disable = None
        with self.assertRaises(ValueError):
            _ = dp.disable

    def test_datapoint_disabled(self):
        dp = DataPoint({"uid": "1.0", "key": "test", "disable": True}, self.device)
        self.assertTrue(dp.disable)

    def test_datapoint_filter_devices(self):
        dp = DataPoint({"uid": "1.0", "key": "test", "filters": {"devices": ["ACL"]}}, self.device)
        self.assertTrue(dp.disable)

    def test_datapoint_filter_devices_match(self):
        dp = DataPoint({"uid": "1.0", "key": "test", "filters": {"devices": ["ASE"]}}, self.device)
        self.assertFalse(dp.disable)

    def test_datapoint_filter_options(self):
        dp = DataPoint({"uid": "1.0", "key": "test", "filters": {"options": {"a": "b"}}}, self.device)
        self.assertTrue(dp.disable)

    def test_datapoint_no_filters(self):
        dp = DataPoint({"uid": "1.0", "key": "test"}, self.device)
        self.assertFalse(dp.disable)

    def test_on_poolaccess_connect(self):
        dp = DataPoint({"uid": "5.10", "key": "test"}, self.device)
        client = MagicMock(spec=PoolAccessClient)
        client.build_topic.return_value = "d02/24ASE2-45678/g/5.10"

        dp.on_poolaccess_connect(client)

        client.build_topic.assert_called_once_with(PoolAccessTopicMode.GET, "5.10")
        client.publish.assert_called_once_with("d02/24ASE2-45678/g/5.10")

    def test_on_poolaccess_message_matching(self):
        dp = DataPoint({"uid": "5.10", "key": "test"}, self.device)
        client = MagicMock(spec=PoolAccessClient)
        client.build_topic.return_value = "d02/24ASE2-45678/v/5.10"

        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/24ASE2-45678/v/5.10"
        message.payload = b'{"v": "42", "t": "5.10"}'

        dp.on_poolaccess_message(client, message)

        self.assertEqual(dp.value, {"v": "42", "t": "5.10"})

    def test_on_poolaccess_message_not_matching(self):
        dp = DataPoint({"uid": "5.10", "key": "test"}, self.device)
        client = MagicMock(spec=PoolAccessClient)
        client.build_topic.return_value = "d02/24ASE2-45678/v/5.10"

        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/24ASE2-45678/v/9.99"
        message.payload = b'{"v": "42"}'

        dp.on_poolaccess_message(client, message)

        self.assertIsNone(dp.value)

    def test_on_poolaccess_message_malformed_payload(self):
        dp = DataPoint({"uid": "5.10", "key": "test"}, self.device)
        client = MagicMock(spec=PoolAccessClient)
        client.build_topic.return_value = "d02/24ASE2-45678/v/5.10"

        message = MagicMock(spec=MQTTMessage)
        message.topic = "d02/24ASE2-45678/v/5.10"
        message.payload = b"{"

        dp.on_poolaccess_message(client, message)

        self.assertIsNone(dp.value)

    def test_value_updated_on_new_message(self):
        dp = DataPoint({"uid": "5.10", "key": "test"}, self.device)
        client = MagicMock(spec=PoolAccessClient)
        client.build_topic.return_value = "d02/24ASE2-45678/v/5.10"

        msg1 = MagicMock(spec=MQTTMessage)
        msg1.topic = "d02/24ASE2-45678/v/5.10"
        msg1.payload = b'{"v": "10"}'
        dp.on_poolaccess_message(client, msg1)
        self.assertEqual(dp.value, {"v": "10"})

        msg2 = MagicMock(spec=MQTTMessage)
        msg2.topic = "d02/24ASE2-45678/v/5.10"
        msg2.payload = b'{"v": "20"}'
        dp.on_poolaccess_message(client, msg2)
        self.assertEqual(dp.value, {"v": "20"})


if __name__ == "__main__":
    unittest.main()
