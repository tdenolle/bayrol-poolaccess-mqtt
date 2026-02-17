import json
import unittest
from unittest.mock import MagicMock, patch

from requests import RequestException
from app.hass.Update import Update
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
import os


class TestUpdate(unittest.TestCase):

    def setUp(self):
        self.device = BayrolPoolaccessDevice("22ASE2-12343")
        self.data = {
            "uid": "6.15",
            "key": "sw_version",
            "name" : "Version"
        }
        

    def test_initialization(self):
        update_entity = Update(self.data, self.device)
        self.assertEqual(update_entity.uid, "6.15")
        self.assertEqual(update_entity.key, "sw_version")
        self.assertEqual(update_entity.type, "update")
        self.assertEqual(update_entity.get_attr("platform"), "update")

    def test_build_config(self):
        update_entity = Update(self.data, self.device)
        config_topic, config_payload = update_entity.build_config()
        self.assertEqual(config_payload["name"], "Version")
        self.assertEqual(config_payload["unique_id"], "bayrol_22ase212343_sw_version")
        self.assertEqual(config_payload["default_entity_id"], "update.bayrol_22ase212343_sw_version")
        self.assertEqual(config_payload["state_topic"], "homeassistant/update/22ASE2-12343/sw_version")
        self.assertIn("availability", config_payload)
        self.assertIn("value_template", config_payload)
        self.assertEqual(config_topic, "homeassistant/update/22ASE2-12343/sw_version/config")

    def test_get_payload(self):
        update_entity = Update(self.data, self.device)
        message = b'{"v": "1.0.0"}'
        payload = update_entity.get_payload(message)
        if payload is None:
            self.fail("payload ne doit pas être None")
        self.assertIn("updatedAt", payload)
        self.assertIn("v", payload)
        self.assertEqual(json.loads(payload)["v"], "1.0.0")

    def test_type_property(self):
        update_entity = Update(self.data, self.device)
        self.assertEqual(update_entity.type, "update")

    @patch("app.hass.Update.requests.get")
    def test_get_update_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = { self.device.model : { "version": "2.0.0", "url": "https://test.url" } }
        mock_get.return_value = mock_response
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {"version": "2.0.0", "url": "https://test.url"})

    @patch("app.hass.Update.requests.get")
    def test_get_update_data_model_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"other_model": {"version": "2.0.0"}}
        mock_get.return_value = mock_response
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {})

    @patch("app.hass.Update.requests.get")
    def test_get_update_data_http_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {})

    @patch("app.hass.Update.requests.get")
    def test_get_update_data_json_decode_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("No JSON")
        mock_get.return_value = mock_response
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {})

    @patch("app.hass.Update.requests.get")
    def test_get_update_data_request_exception(self, mock_get):
        mock_get.side_effect = RequestException("Network error")
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {})

    @patch.dict(os.environ, {"APP_VERSION": "9.9.9"})
    @patch("app.hass.Update.requests.get")
    def test_get_update_data_with_env_version(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = { self.device.model : {"version": "2.0.0"}}
        mock_get.return_value = mock_response
        Update(self.data, self.device)
        mock_get.assert_called_with(
            Update.BAYROL_UPDATE_URL,
            params={"id": self.device.id, "version": "9.9.9"},
            timeout=5,
            allow_redirects=False
        )

    def test_value_template_in_attributes(self):
        update_entity = Update(self.data, self.device)
        value_template = update_entity.get_attr("value_template")
        if value_template is None:
            self.fail("value_template ne doit pas être None")
        self.assertIn("installed_version", value_template)
        self.assertIn("latest_version", value_template)
        self.assertIn("release_url", value_template)


if __name__ == '__main__':
    unittest.main()
