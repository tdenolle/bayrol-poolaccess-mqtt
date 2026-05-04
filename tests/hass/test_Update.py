import json
import unittest
from unittest.mock import MagicMock, patch, ANY

from requests import RequestException
from app.hass.Update import Update
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.mqtt.MqttClient import MqttClient
from app.mqtt.PoolAccessClient import PoolAccessClient
import os


class TestUpdate(unittest.TestCase):

    def setUp(self):
        self.device = BayrolPoolaccessDevice("22ASE2-12343")
        self.data = {
            "uid": "6.15",
            "key": "sw_version",
            "name" : "Version"
        }
        self.patcher = patch("app.hass.Update.requests.get")
        self.mock_get = self.patcher.start()
        self.mock_get.return_value = MagicMock(status_code=404)
        self.addCleanup(self.patcher.stop)

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

    @patch.dict(os.environ, {"UPDATE_VERSION_ENDPOINT": "http://mocked/endpoint"})
    def test_get_update_data_success(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Bayrol Automatic Salt",
            "url": "https://www.bayrol.fr/support-technique/automatic-salt",
            "version": "v2.50 (260203-0001)"
        }
        self.mock_get.return_value = mock_response
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {
            "name": "Bayrol Automatic Salt",
            "url": "https://www.bayrol.fr/support-technique/automatic-salt",
            "version": "v2.50 (260203-0001)"
        })

    def test_get_update_data_no_endpoint(self):
        # UPDATE_VERSION_ENDPOINT not set → returns {} without calling requests.get
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.mock_get.assert_not_called()
        self.assertEqual(data, {})

    @patch.dict(os.environ, {"UPDATE_VERSION_ENDPOINT": "http://mocked/endpoint"})
    def test_get_update_data_http_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 404
        self.mock_get.return_value = mock_response
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {})

    @patch.dict(os.environ, {"UPDATE_VERSION_ENDPOINT": "http://mocked/endpoint"})
    def test_get_update_data_json_decode_error(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("No JSON")
        self.mock_get.return_value = mock_response
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {})

    @patch.dict(os.environ, {"UPDATE_VERSION_ENDPOINT": "http://mocked/endpoint"})
    def test_get_update_data_request_exception(self):
        self.mock_get.side_effect = RequestException("Network error")
        update_entity = Update(self.data, self.device)
        data = update_entity._get_update_data(self.device)
        self.assertEqual(data, {})

    @patch.dict(os.environ, {"APP_VERSION": "9.9.9", "UPDATE_VERSION_ENDPOINT": "http://test/endpoint"})
    def test_get_update_data_with_env_version(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Bayrol Automatic Salt",
            "url": "https://www.bayrol.fr/support-technique/automatic-salt",
            "version": "v2.50 (260203-0001)"
        }
        self.mock_get.return_value = mock_response
        Update(self.data, self.device)
        self.mock_get.assert_called_with(
            "http://test/endpoint",
            headers={"User-Agent": "BayrolPoolaccess/9.9.9"},
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

    def test_value_template_fallback_when_no_update_data(self):
        # No endpoint set → update_data = {} → fallback to "unavailable" and DEFAULT_BAYROL_SUPPORT_URL
        update_entity = Update(self.data, self.device)
        value_template = update_entity.get_attr("value_template")
        self.assertIn("unavailable", value_template)
        self.assertIn(Update.DEFAULT_BAYROL_SUPPORT_URL, value_template)

    @patch.dict(os.environ, {"UPDATE_VERSION_ENDPOINT": "http://mocked/endpoint"})
    def test_value_template_uses_update_data(self):
        # Endpoint set, valid response → value_template uses version and url from response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Bayrol Automatic Salt",
            "url": "https://www.bayrol.fr/support-technique/automatic-salt",
            "version": "v2.50 (260203-0001)"
        }
        self.mock_get.return_value = mock_response
        update_entity = Update(self.data, self.device)
        value_template = update_entity.get_attr("value_template")
        self.assertIn("v2.50 (260203-0001)", value_template)
        self.assertIn("https://www.bayrol.fr/support-technique/automatic-salt", value_template)

    @patch.dict(os.environ, {"UPDATE_VERSION_ENDPOINT": "http://mocked/endpoint"})
    def test_on_periodic_refresh(self):
        """Test that on_periodic_refresh re-fetches update data and republishes config + GET."""
        # Initial creation with no update data
        update_entity = Update(self.data, self.device)

        # Now mock a successful response for refresh
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "version": "v3.00 (260301-0001)",
            "url": "https://www.bayrol.fr/support-technique/new-version"
        }
        self.mock_get.return_value = mock_response

        mock_poolaccess = MagicMock(spec=PoolAccessClient)
        mock_broker = MagicMock(spec=MqttClient)

        update_entity.on_periodic_refresh(mock_poolaccess, mock_broker)

        # Check value_template was updated
        value_template = update_entity.get_attr("value_template")
        self.assertIn("v3.00 (260301-0001)", value_template)
        self.assertIn("https://www.bayrol.fr/support-technique/new-version", value_template)

        # Check config was published to broker
        mock_broker.publish.assert_called_once_with(
            "homeassistant/update/22ASE2-12343/sw_version/config",
            payload=ANY,
            retain=True
        )

        # Check GET was published to poolaccess
        mock_poolaccess.publish.assert_called_once()

    @patch.dict(os.environ, {"UPDATE_VERSION_ENDPOINT": "http://mocked/endpoint"})
    def test_on_periodic_refresh_with_http_failure(self):
        """Test that on_periodic_refresh falls back gracefully on HTTP failure."""
        update_entity = Update(self.data, self.device)

        # Mock a failed response for refresh
        self.mock_get.return_value = MagicMock(status_code=500)

        mock_poolaccess = MagicMock(spec=PoolAccessClient)
        mock_broker = MagicMock(spec=MqttClient)

        update_entity.on_periodic_refresh(mock_poolaccess, mock_broker)

        # Check value_template falls back to unavailable
        value_template = update_entity.get_attr("value_template")
        self.assertIn("unavailable", value_template)

        # Config and GET should still be published
        mock_broker.publish.assert_called_once()
        mock_poolaccess.publish.assert_called_once()


if __name__ == '__main__':
    unittest.main()
