import unittest

from app.hass.Entity import Entity
from app.hass.Sensor import Sensor
from app.hass.Switch import Switch


class TestEntity(unittest.TestCase):
    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "1.0", "key": "test_entity", "name": "Test Entity"}

    def test_entity_creation(self):
        # Test creating a Entity instance
        entity = Entity(self.json_data)
        self.assertEqual(entity.uid, "1.0")
        self.assertEqual(entity.key, "test_entity")
        self.assertEqual(entity.name, "Test Entity")
        self.assertEqual(entity.attributes, {})
        with self.assertRaises(NotImplementedError):
            return entity.type

if __name__ == "__main__":
    unittest.main()
