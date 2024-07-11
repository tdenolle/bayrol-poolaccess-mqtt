import unittest
import json

from app.hass.MessagesSensor import MessagesSensor


class TestMessagesSensor(unittest.TestCase):

    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "123", "key": "test", "name": "Test", "test": "test"}

    def test_get_payload_with_valid_message(self):
        sensor = MessagesSensor(self.json_data)
        message = '{"v": ["8.33"]}'
        expected_payload = '{"v": [{"message": "Tout va bien. Profitez de votre piscine !", "type": "success"}]}'
        self.assertEqual(sensor.get_payload(message), expected_payload)

    def test_get_payload_with_multiple_messages(self):
        sensor = MessagesSensor(self.json_data)
        message = '{"v": ["8.33", "8.19"]}'
        expected_payload = '{"v": [{"message": "Tout va bien. Profitez de votre piscine !", "type": "success"}, {"message": "Taux de sel trop bas\\n! Electrolyse arr\\u00eat\\u00e9e !", "type": "warning"}]}'
        self.assertEqual(sensor.get_payload(message), expected_payload)

    def test_get_payload_with_invalid_message(self):
        sensor = MessagesSensor(self.json_data)
        message = '{"v": ["8.99"]}'
        self.assertIsNotNone(sensor.get_payload(message))

    def test_get_payload_with_no_message(self):
        sensor = MessagesSensor(self.json_data)
        self.assertIsNone(sensor.get_payload())


if __name__ == '__main__':
    unittest.main()
