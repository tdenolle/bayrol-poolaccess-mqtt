import unittest

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Sensor import Sensor
from app.hass.Switch import Switch


class TestSwitch(unittest.TestCase):
    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "1.19", "key": "sw_on_off", "name": "Switch ON/OFF", "json_attributes_template": "{}"}
        self.device = BayrolPoolaccessDevice("22ASE-12343")

    def test_switch_creation(self):
        # Test creating a Switch instance
        switch = Switch(self.json_data, self.device)
        self.assertEqual(switch.uid, "1.19")
        self.assertEqual(switch.key, "sw_on_off")
        self.assertEqual(switch.type, "switch")
        self.assertEqual(switch.name, "Switch ON/OFF")


    def test_switch_config(self):
        # Test building switch configuration
        switch = Switch(self.json_data,self.device)
        config_topic, config = switch.build_config()
        expected_config = {
            'availability': [{'topic': 'homeassistant/sensor/22ASE-12343/status',
                              'value_template': "{{ 'online' if value_json.v | float > "
                                                "17.0 else 'offline' }}"}],
            'command_topic': 'homeassistant/switch/22ASE-12343/sw_on_off/set',
            'device': self.device,
            'json_attributes_template': '{}',
            'json_attributes_topic': 'homeassistant/switch/22ASE-12343/sw_on_off',
            'name': 'Switch ON/OFF',
            'state_topic': 'homeassistant/switch/22ASE-12343/sw_on_off',
            'unique_id': 'bayrol_22ase12343_sw_on_off',
            'object_id': 'bayrol_22ase12343_sw_on_off',
            'value_template': '{{ value_json.v }}',
            'payload_off': 'off',
            'payload_on': 'on'
        }
        self.assertEqual(config_topic, "homeassistant/switch/22ASE-12343/sw_on_off/config")
        self.assertEqual(config, expected_config)


if __name__ == "__main__":
    unittest.main()
