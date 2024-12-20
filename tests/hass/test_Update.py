import json
import unittest
from unittest.mock import MagicMock
from app.hass.Update import Update
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice


class TestUpdate(unittest.TestCase):

    def setUp(self):
        self.device = BayrolPoolaccessDevice("22ASE-12343")
        self.data = {
            "uid": "6.15",
            "key": "sw_version",
            "name" : "Version",
            "value_template": "{{ value_json.v }}"
        }
        self.update_entity = Update(self.data, self.device)

    def test_initialization(self):
        self.assertEqual(self.update_entity.uid, "6.15")
        self.assertEqual(self.update_entity.key, "sw_version")
        self.assertEqual(self.update_entity.type, "update")
        self.assertEqual(self.update_entity.get_attr("platform"), "update")

    def test_build_config(self):
        config_topic, config_payload = self.update_entity.build_config()
        expected_config = {'availability': [{'topic': 'homeassistant/sensor/22ASE-12343/status',
                   'value_template': "{{ 'online' if value_json.v | float > "
                                     "17.0 else 'offline' }}"}],
 'device': self.device,
 'name': 'Version',
 'object_id': 'bayrol_22ase12343_sw_version',
 'platform': 'update',
 'state_topic': 'homeassistant/update/22ASE-12343/sw_version',
 'unique_id': 'bayrol_22ase12343_sw_version',
 'value_template': '{{ value_json.v }}'}
        self.assertEqual(config_topic, "homeassistant/update/22ASE-12343/sw_version/config")
        self.assertEqual(config_payload, expected_config)

    def test_get_payload(self):
        message = b'{"v": "1.0.0"}'
        payload = self.update_entity.get_payload(message)
        self.assertIn("updatedAt", payload)
        self.assertIn("v", payload)
        self.assertEqual(json.loads(payload)["v"], "1.0.0")


if __name__ == '__main__':
    unittest.main()
