import unittest

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Sensor import Sensor


class TestSensor(unittest.TestCase):
    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "123", "key": "temperature", "name": "Temperature Sensor", "json_attributes_template" : "{}", "v": "20.5"}
        self.device = BayrolPoolaccessDevice("22ASE-12343")
    def test_sensor_creation(self):
        # Test creating a Sensor instance
        sensor = Sensor(self.json_data,self.device)
        self.assertEqual(sensor.uid, "123")
        self.assertEqual(sensor.key, "temperature")
        self.assertEqual(sensor.type, "sensor")
        self.assertEqual(sensor.name, "Temperature Sensor")

    def test_sensor_config(self):
        # Test building sensor configuration
        sensor = Sensor(self.json_data,self.device)
        config_topic, config = sensor.build_config()
        expected_config = {
            "unique_id": "bayrol_22ase12343_temperature",
            'default_entity_id': 'sensor.bayrol_22ase12343_temperature',
            "name": "Temperature Sensor",
            "state_topic": "homeassistant/sensor/22ASE-12343/temperature",
            "availability": [
                {
                    "topic": "homeassistant/sensor/22ASE-12343/status",
                    "value_template": "{{ 'online' if value_json.v | float > 17.0 else 'offline' }}"
                }
            ],
            "v": "20.5",
            "json_attributes_template": "{}",
            "json_attributes_topic": "homeassistant/sensor/22ASE-12343/temperature",
            "value_template": "{{ value_json.v }}",
            "device": self.device
        }
        self.assertEqual(config_topic, "homeassistant/sensor/22ASE-12343/temperature/config")
        self.assertEqual(config, expected_config)


if __name__ == "__main__":
    unittest.main()
