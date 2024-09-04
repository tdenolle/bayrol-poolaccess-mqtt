import unittest

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity
from app.hass.Sensor import Sensor
from app.hass.Switch import Switch


class TestEntity(unittest.TestCase):
    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "1.0", "key": "test_entity", "name": "Test Entity"}
        self.device = BayrolPoolaccessDevice("1.0")

    def test_entity_creation(self):
        with self.assertRaises(NotImplementedError):
            Entity(self.json_data, self.device)

if __name__ == "__main__":
    unittest.main()



