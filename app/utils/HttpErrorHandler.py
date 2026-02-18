#!/usr/bin/env python3

"""
Custom logging handler that sends error-level log records to a remote HTTP API.
Sends each error asynchronously in a separate thread to avoid blocking the application.
"""

import datetime
import logging
import threading
import traceback

import requests


class HttpErrorHandler(logging.Handler):
    """
    A logging handler that forwards ERROR+ log records to a remote API via HTTP POST.

    Features:
        - Asynchronous: each log record is sent in a background thread
        - Resilient: network failures are silently ignored (logged to stdout as WARNING)
        - Anti-recursion: prevents infinite loops if the HTTP call itself logs an error

    Args:
        url: The remote API endpoint URL (HTTP POST)
        device_serial: The device serial number included in the payload for identification
        app_version: The application version string included in the payload
        timeout: HTTP request timeout in seconds (default: 5)
        level: Minimum log level to capture (default: ERROR)
    """

    def __init__(self, url: str, device_serial: str = "", app_version: str = "unknown", timeout: int = 5, level: int = logging.ERROR):
        super().__init__(level)
        self._url = url
        self._device_serial = device_serial
        self._app_version = app_version
        self._timeout = timeout
        self._sending = threading.local()

    def emit(self, record: logging.LogRecord):
        """Emit a log record by sending it to the remote API in a background thread."""
        # Anti-recursion guard: skip if we're already inside a send
        if getattr(self._sending, 'active', False):
            return

        try:
            payload = self._build_payload(record)
            thread = threading.Thread(target=self._send, args=(payload,), daemon=True)
            thread.start()
        except Exception:
            self.handleError(record)

    def _build_payload(self, record: logging.LogRecord) -> dict:
        """Build the JSON payload from a log record."""
        tb = None
        if record.exc_info and record.exc_info[1] is not None:
            tb = ''.join(traceback.format_exception(*record.exc_info))

        return {
            "timestamp": datetime.datetime.fromtimestamp(record.created, tz=datetime.timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
            "traceback": tb,
            "device_serial": self._device_serial,
            "app_version": self._app_version,
        }

    def _send(self, payload: dict):
        """Send the payload to the remote API. Runs in a background thread."""
        self._sending.active = True
        try:
            response = requests.post(self._url, json=payload, timeout=self._timeout)
            if response.status_code >= 400:
                logging.getLogger(__name__).warning(
                    "Error reporting failed with status %s", response.status_code
                )
        except requests.RequestException as e:
            logging.getLogger(__name__).warning("Error reporting request failed: %s", str(e))
        finally:
            self._sending.active = False
