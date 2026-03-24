import unittest
from unittest.mock import MagicMock, patch

from app.Translation import LanguageManager
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity
from app.mqtt.MqttClient import MqttClient
from app.mqtt.PoolAccessClient import PoolAccessClient


class TestEntity(unittest.TestCase):
    def setUp(self):
        # Example JSON data for testing
        self.json_data = {"uid": "1.0", "key": "test_entity", "name": "Test Entity"}
        self.device = BayrolPoolaccessDevice("1.0")
        LanguageManager().setup("en")

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

    @patch('app.hass.Entity.threading.Timer')
    def test_start_periodic_refresh_with_interval(self, mock_timer_class):
        class DummyEntity(Entity):
            @property
            def type(self):
                return "dummy"

        entity = DummyEntity({"uid": "1", "key": "test", "check_interval": 2}, BayrolPoolaccessDevice("1.0"))
        mock_timer = MagicMock()
        mock_timer_class.return_value = mock_timer
        mock_pa = MagicMock(spec=PoolAccessClient)
        mock_broker = MagicMock(spec=MqttClient)

        entity.start_periodic_refresh(mock_pa, mock_broker)

        mock_timer_class.assert_called_once_with(2 * 3600, entity._do_periodic_refresh, args=(mock_pa, mock_broker))
        mock_timer.start.assert_called_once()
        self.assertTrue(mock_timer.daemon)

    def test_start_periodic_refresh_without_interval(self):
        class DummyEntity(Entity):
            @property
            def type(self):
                return "dummy"

        entity = DummyEntity({"uid": "1", "key": "test"}, BayrolPoolaccessDevice("1.0"))
        with patch('app.hass.Entity.threading.Timer') as mock_timer_class:
            entity.start_periodic_refresh(MagicMock(), MagicMock())
            mock_timer_class.assert_not_called()

    @patch('app.hass.Entity.threading.Timer')
    def test_do_periodic_refresh_calls_on_periodic_refresh_and_reschedules(self, mock_timer_class):
        class DummyEntity(Entity):
            @property
            def type(self):
                return "dummy"

        entity = DummyEntity({"uid": "1", "key": "test", "check_interval": 1}, BayrolPoolaccessDevice("1.0"))
        entity.on_periodic_refresh = MagicMock()
        mock_pa = MagicMock(spec=PoolAccessClient)
        mock_broker = MagicMock(spec=MqttClient)

        entity._do_periodic_refresh(mock_pa, mock_broker)

        entity.on_periodic_refresh.assert_called_once_with(mock_pa, mock_broker)
        # Timer should be created for rescheduling
        self.assertEqual(mock_timer_class.call_count, 1)

    @patch('app.hass.Entity.threading.Timer')
    def test_stop_periodic_refresh(self, mock_timer_class):
        class DummyEntity(Entity):
            @property
            def type(self):
                return "dummy"

        entity = DummyEntity({"uid": "1", "key": "test", "check_interval": 1}, BayrolPoolaccessDevice("1.0"))
        mock_timer = MagicMock()
        entity._refresh_timer = mock_timer

        entity.stop_periodic_refresh()

        mock_timer.cancel.assert_called_once()
        self.assertIsNone(entity._refresh_timer)


if __name__ == "__main__":
    unittest.main()



