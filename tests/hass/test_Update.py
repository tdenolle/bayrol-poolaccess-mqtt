import json
import unittest
from unittest.mock import MagicMock
from app.hass.Update import Update
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice


class TestUpdate(unittest.TestCase):

    def setUp(self):
        self.device = BayrolPoolaccessDevice("22ASE2-12343")
        self.data = {
            "uid": "6.15",
            "key": "sw_version",
            "name" : "Version"
        }
        self.update_entity = Update(self.data, self.device)

    def test_initialization(self):
        self.assertEqual(self.update_entity.uid, "6.15")
        self.assertEqual(self.update_entity.key, "sw_version")
        self.assertEqual(self.update_entity.type, "update")
        self.assertEqual(self.update_entity.get_attr("platform"), "update")

    def test_build_config(self):
        config_topic, config_payload = self.update_entity.build_config()
        self.assertEqual(config_payload["name"], "Version")
        self.assertEqual(config_payload["unique_id"], "bayrol_22ase212343_sw_version")
        self.assertEqual(config_payload["object_id"], "bayrol_22ase212343_sw_version")
        self.assertEqual(config_payload["state_topic"], "homeassistant/update/22ASE2-12343/sw_version")
        self.assertIn("availability", config_payload)
        self.assertIn("value_template", config_payload)
        self.assertEqual(config_topic, "homeassistant/update/22ASE2-12343/sw_version/config")

    def test_get_payload(self):
        message = b'{"v": "1.0.0"}'
        payload = self.update_entity.get_payload(message)
        self.assertIn("updatedAt", payload)
        self.assertIn("v", payload)
        self.assertEqual(json.loads(payload)["v"], "1.0.0")


if __name__ == '__main__':
    unittest.main()
