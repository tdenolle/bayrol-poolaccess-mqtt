import unittest

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice, get_device_model_from_serial


class TestBayrolPoolaccessDevice(unittest.TestCase):
    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "1.0", "key": "test_entity", "name": "Test Entity"}
        self.device = BayrolPoolaccessDevice("1.0")

    def test_get_device_model_from_serial_automatic_salt(self):
        self.assertEqual(get_device_model_from_serial("12ASE1-12345"), "Automatic Salt")


    def test_get_device_model_from_serial_automatic_cl_ph(self):
        self.assertEqual(get_device_model_from_serial("12ACL1-12345"), "Automatic Cl-pH")


    def test_get_device_model_from_serial_automatic_ph(self):
        self.assertEqual(get_device_model_from_serial("12APH1-12345"), "Automatic pH")


    def test_get_device_model_from_serial_unknown(self):
        self.assertEqual(get_device_model_from_serial("12ABC1-12345"), "Unknown")


    def test_get_device_model_from_serial_invalid_format(self):
        self.assertEqual(get_device_model_from_serial("12345"), "Unknown")

if __name__ == "__main__":
    unittest.main()
