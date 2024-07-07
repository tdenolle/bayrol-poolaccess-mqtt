import unittest
from unittest.mock import patch, MagicMock

from paho.mqtt.enums import MQTTErrorCode

from app.mqtt.MqttClient import MqttClient


class TestMqttClient(unittest.TestCase):

    def setUp(self):
        self.host = "test_host"
        self.port = 1234
        self.user = "test_user"
        self.password = "test_password"
        self.transport = "tcp"
        self.client = MqttClient(self.host, self.port, self.user, self.password, self.transport)

    def test_init(self):
        self.assertEqual(self.client._host, self.host)
        self.assertEqual(self.client._port, self.port)
        self.assertEqual(self.client._user, self.user)
        self.assertEqual(self.client._pwd, self.password)
        self.assertEqual(self.client._transport, self.transport)
        self.assertIsNotNone(self.client._cid)
        self.assertTrue(self.client._cid.startswith('user_'))

    @patch('paho.mqtt.client.Client.username_pw_set')
    def test_init_with_credentials(self, mock_username_pw_set):
        MqttClient(self.host, self.port, self.user, self.password, self.transport)
        mock_username_pw_set.assert_called_once_with(self.user, self.password)

    @patch('paho.mqtt.client.Client.connect')
    def test_establish_connection(self, mock_connect):
        self.client.establish_connection()
        mock_connect.assert_called_once_with(self.host, self.port)

    @patch('paho.mqtt.client.Client.on_connect')
    def test_on_connect(self, mock_on_connect):
        self.client.on_connect(None, None, None, 0)
        mock_on_connect.assert_called_once_with(None, None, None, 0)

    @patch('paho.mqtt.client.Client.on_message')
    def test_on_message(self, mock_on_message):
        self.client.on_message(None, None, None)
        mock_on_message.assert_called_once_with(None, None, None)

    @patch('paho.mqtt.client.Client.on_disconnect')
    def test_on_disconnect(self, mock_on_disconnect):
        self.client.on_disconnect(None, None, None)
        mock_on_disconnect.assert_called_once_with(None, None, None)

    @patch('paho.mqtt.client.Client.publish')
    def test_publish(self, mock_publish):
        self.client.publish("test_topic", "test_payload", 0, False)
        mock_publish.assert_called_once_with("test_topic", "test_payload", 0, False)

    @patch('paho.mqtt.client.Client.subscribe')
    def test_subscribe(self, mock_subscribe):
        self.client.subscribe("test_topic", 0)
        mock_subscribe.assert_called_once_with("test_topic", 0)

    @patch('paho.mqtt.client.Client.loop_start')
    def test_loop_start(self, mock_loop_start):
        self.client.loop_start()
        mock_loop_start.assert_called_once()

    @patch('paho.mqtt.client.Client.loop_stop')
    def test_loop_stop(self, mock_loop_stop):
        self.client.loop_stop()
        mock_loop_stop.assert_called_once()

    @patch('paho.mqtt.client.Client.loop_forever')
    def test_loop_forever(self, mock_loop_forever):
        self.client.loop_forever()
        mock_loop_forever.assert_called_once()

    @patch('paho.mqtt.client.Client.connect')
    def test_establish_connection_success(self, mock_connect):
        mock_connect.return_value = 0
        result = self.client.establish_connection()
        self.assertEqual(result, MQTTErrorCode.MQTT_ERR_SUCCESS)
        mock_connect.assert_called_once_with(self.host, self.port)

    @patch('paho.mqtt.client.Client.connect')
    def test_establish_connection_failure(self, mock_connect):
        mock_connect.side_effect = ConnectionRefusedError("Connection refused")
        result = self.client.establish_connection()
        self.assertEqual(result, MQTTErrorCode.MQTT_ERR_CONN_REFUSED)
        mock_connect.assert_called_once_with(self.host, self.port)


if __name__ == '__main__':
    unittest.main()
