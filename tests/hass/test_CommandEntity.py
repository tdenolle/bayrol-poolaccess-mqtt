import unittest
from app.hass.CommandEntity import CommandEntity
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice

class TestCommandEntity(unittest.TestCase):
    def setUp(self):
        self.data = {"uid": "1.0", "key": "test_command", "name": "Test Command", "state_topic": "test/state"}
        self.device = BayrolPoolaccessDevice("1.0")
  
    def test_type_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            CommandEntity(self.data, self.device).type

if __name__ == "__main__":
    unittest.main() 