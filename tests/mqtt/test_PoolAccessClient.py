import unittest
from unittest.mock import patch, MagicMock
from bayrol_poolaccess_mqtt.mqtt.PoolAccessClient import PoolAccessClient, BAYROL_POOLACCESS_MQTT_HOST, \
    BAYROL_POOLACCESS_MQTT_PORT, BAYROL_POOLACCESS_MQTT_TRANSPORT, BAYROL_POOLACCESS_MQTT_PASSWORD


class TestPoolAccessClient(unittest.TestCase):

    def setUp(self):
        self.token = "test_token"
        self.client = PoolAccessClient(self.token)

    @patch('paho.mqtt.client.Client.tls_set')
    def test_tls_set(self, mock_mqtt_client_tls_set):
        PoolAccessClient(self.token)
        mock_mqtt_client_tls_set.assert_called_once()

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


if __name__ == '__main__':
    unittest.main()
