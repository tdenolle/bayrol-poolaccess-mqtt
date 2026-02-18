import logging
import unittest
from unittest.mock import patch, MagicMock, ANY

from app.utils.HttpErrorHandler import HttpErrorHandler


class TestHttpErrorHandler(unittest.TestCase):

    def setUp(self):
        self.url = "https://api.example.com/errors"
        self.device_serial = "24ASE2-45678"
        self.app_version = "1.4.5"
        self.handler = HttpErrorHandler(
            url=self.url,
            device_serial=self.device_serial,
            app_version=self.app_version,
            timeout=3,
        )
        # Create a logger with the handler for testing
        self.logger = logging.getLogger("test_http_error_handler")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)

    def tearDown(self):
        self.logger.removeHandler(self.handler)

    def test_handler_level_is_error(self):
        """Handler should only capture ERROR and above."""
        self.assertEqual(self.handler.level, logging.ERROR)

    def test_build_payload_basic(self):
        """Payload should contain all expected fields."""
        record = logging.LogRecord(
            name="test.module",
            level=logging.ERROR,
            pathname="test_file.py",
            lineno=42,
            msg="Something went wrong",
            args=None,
            exc_info=None,
        )
        payload = self.handler._build_payload(record)

        self.assertEqual(payload["level"], "ERROR")
        self.assertEqual(payload["message"], "Something went wrong")
        self.assertEqual(payload["logger"], "test.module")
        self.assertEqual(payload["lineno"], 42)
        self.assertEqual(payload["device_serial"], self.device_serial)
        self.assertEqual(payload["app_version"], self.app_version)
        self.assertIn("timestamp", payload)
        self.assertIsNone(payload["traceback"])

    def test_build_payload_with_exception(self):
        """Payload should include traceback when exception info is present."""
        try:
            raise ValueError("test error")
        except ValueError:
            import sys
            exc_info = sys.exc_info()

        record = logging.LogRecord(
            name="test.module",
            level=logging.ERROR,
            pathname="test_file.py",
            lineno=10,
            msg="Error with exception",
            args=None,
            exc_info=exc_info,
        )
        payload = self.handler._build_payload(record)

        self.assertIsNotNone(payload["traceback"])
        self.assertIn("ValueError", payload["traceback"])
        self.assertIn("test error", payload["traceback"])

    @patch("app.utils.HttpErrorHandler.requests.post")
    def test_emit_sends_post_request(self, mock_post):
        """emit() should trigger an HTTP POST with the correct payload."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        record = logging.LogRecord(
            name="test.module",
            level=logging.ERROR,
            pathname="test_file.py",
            lineno=42,
            msg="Test error message",
            args=None,
            exc_info=None,
        )
        # Call _send directly to test synchronously (emit spawns a thread)
        payload = self.handler._build_payload(record)
        self.handler._send(payload)

        mock_post.assert_called_once_with(
            self.url,
            json=ANY,
            timeout=3,
        )
        sent_payload = mock_post.call_args[1]["json"]
        self.assertEqual(sent_payload["message"], "Test error message")
        self.assertEqual(sent_payload["level"], "ERROR")
        self.assertEqual(sent_payload["device_serial"], self.device_serial)

    @patch("app.utils.HttpErrorHandler.requests.post")
    def test_emit_handles_network_failure_gracefully(self, mock_post):
        """Network failures should not raise exceptions."""
        import requests as req
        mock_post.side_effect = req.RequestException("Connection refused")

        payload = {
            "timestamp": "2026-02-18T10:00:00+00:00",
            "level": "ERROR",
            "message": "test",
            "logger": "test",
            "module": "test",
            "funcName": "test",
            "lineno": 1,
            "traceback": None,
            "device_serial": self.device_serial,
        }

        # Should not raise
        self.handler._send(payload)

    @patch("app.utils.HttpErrorHandler.requests.post")
    def test_emit_handles_http_error_status(self, mock_post):
        """HTTP 4xx/5xx should log a warning but not raise."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        payload = {
            "timestamp": "2026-02-18T10:00:00+00:00",
            "level": "ERROR",
            "message": "test",
            "logger": "test",
            "module": "test",
            "funcName": "test",
            "lineno": 1,
            "traceback": None,
            "device_serial": self.device_serial,
        }

        # Should not raise
        self.handler._send(payload)
        mock_post.assert_called_once()

    def test_info_and_warning_not_captured(self):
        """INFO and WARNING logs should not trigger the handler."""
        with patch.object(self.handler, 'emit') as mock_emit:
            self.logger.info("Info message")
            self.logger.warning("Warning message")
            mock_emit.assert_not_called()

    def test_error_is_captured(self):
        """ERROR logs should trigger the handler."""
        with patch.object(self.handler, 'emit') as mock_emit:
            self.logger.error("Error message")
            mock_emit.assert_called_once()

    def test_critical_is_captured(self):
        """CRITICAL logs should trigger the handler."""
        with patch.object(self.handler, 'emit') as mock_emit:
            self.logger.critical("Critical message")
            mock_emit.assert_called_once()

    @patch("app.utils.HttpErrorHandler.requests.post")
    def test_emit_spawns_thread(self, mock_post):
        """emit() should spawn a daemon thread for sending."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        with patch("app.utils.HttpErrorHandler.threading.Thread") as mock_thread:
            mock_thread_instance = MagicMock()
            mock_thread.return_value = mock_thread_instance

            record = logging.LogRecord(
                name="test", level=logging.ERROR,
                pathname="test.py", lineno=1,
                msg="test", args=None, exc_info=None,
            )
            self.handler.emit(record)

            mock_thread.assert_called_once()
            self.assertTrue(mock_thread.call_args[1].get("daemon", False))
            mock_thread_instance.start.assert_called_once()


if __name__ == '__main__':
    unittest.main()
