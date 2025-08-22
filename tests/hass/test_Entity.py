import unittest

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class TestEntity(unittest.TestCase):
    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "1.0", "key": "test_entity", "name": "Test Entity"}
        self.device = BayrolPoolaccessDevice("1.0")

    def test_entity_creation(self):
        with self.assertRaises(NotImplementedError):
            Entity(self.json_data, self.device)

    def test_key_and_disable_value_error(self):
        class DummyEntity(Entity):
            @property
            def type(self):
                return "dummy"

        device = BayrolPoolaccessDevice("1.0")
        json_data = {"uid": "1.0", "name": "Test Entity"}
        entity = object.__new__(DummyEntity)
        entity._key = None
        entity._disable = None
        entity._attributes = {"name": "Test Entity", "state_topic": "topic"}
        with self.assertRaises(ValueError):
            _ = entity.key
        with self.assertRaises(ValueError):
            _ = entity.disable


if __name__ == "__main__":
    unittest.main()



