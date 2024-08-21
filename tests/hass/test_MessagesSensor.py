import re
import unittest
import json

from app.hass.MessagesSensor import MessagesSensor


class TestMessagesSensor(unittest.TestCase):

    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "123", "key": "test", "name": "Test", "test": "test"}

    def test_get_payload_with_valid_message(self):
        sensor = MessagesSensor(self.json_data)
        message = b'{"v": ["8.33"]}'
        actual_payload = sensor.get_payload(message)
        updatedAt = self.get_attribute_value_in_payload(actual_payload, "updatedAt")
        expected_payload = ('{"v": [{"message": "Tout va bien. Profitez de votre piscine !", "type": "success"}], '
                            '"updatedAt": "%s"}') % updatedAt
        self.assertEqual(actual_payload, expected_payload)

    def test_get_payload_with_multiple_messages(self):
        sensor = MessagesSensor(self.json_data)
        message = b'{"v": ["8.33", "8.19"]}'
        actual_payload = sensor.get_payload(message)
        updatedAt = self.get_attribute_value_in_payload(actual_payload,"updatedAt")
        expected_payload = ('{"v": [{"message": "Tout va bien. Profitez de votre piscine !", "type": "success"}, '
                            '{"message": "Taux de sel trop bas\\n! Electrolyse arr\\u00eat\\u00e9e !", '
                            '"type": "warning"}], "updatedAt": "%s"}') % updatedAt

        self.assertEqual(actual_payload, expected_payload)

    def test_get_payload_with_invalid_message(self):
        sensor = MessagesSensor(self.json_data)
        message = '{"v": ["8.99"]}'
        self.assertIsNotNone(sensor.get_payload(message))

    def test_get_payload_with_no_message(self):
        sensor = MessagesSensor(self.json_data)
        self.assertIsNone(sensor.get_payload())

    def get_attribute_value_in_payload(self, payload, attr_name):
        # use a regular expression to get attribute in payload string
        match = re.search(r'"%s": "(.*?)"' % attr_name, payload)
        if match:
            return match.group(1)
        # use regex to get attribute in payload string
        return "Not Found"

if __name__ == '__main__':
    unittest.main()
