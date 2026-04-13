#!/usr/bin/env python3
import json
import logging
from json import JSONDecodeError

from paho.mqtt.client import MQTTMessage

from app.hass import load_attr
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.mqtt.PoolAccessClient import PoolAccessClient, PoolAccessTopicMode


class DataPoint:
    """Base class for PoolAccess data points.

    Stores values received from the PoolAccess MQTT server for internal use.
    Unlike Entity, DataPoint values are NOT bridged to the Home Assistant MQTT broker.
    """

    def __init__(self, data: dict, device: BayrolPoolaccessDevice):
        self._uid = load_attr("uid", data, True)
        self._key = load_attr("key", data)
        self._device = device
        self._logger = logging.getLogger()
        self._disable = False
        self._value = None

        if "disable" in data:
            self._disable = load_attr("disable", data, False)
            if self._disable:
                self._logger.info("'%s' is disabled", self._key)

        if not self._disable:
            filters = load_attr("filters", data, True)

            if filters is None:
                self._logger.debug("Filters are not set")
                return

            # device filtering check
            devices = filters["devices"] if "devices" in filters else []
            if len(devices) > 0 and self._device.code not in devices:
                self._logger.info(
                    "Skipping '%s' because device '%s' is in filter devices %s", self._key, self._device.code,
                    devices)
                self._disable = True

            # options filtering check
            if not self._disable:
                options = filters["options"] if "options" in filters else {}
                for o in options:
                    if o != options[o]:
                        self._logger.info(
                            "Skipping '%s' because filter option '%s' is not set or not matching value '%s'",
                            self._key, o, options[o])
                        self._disable = True

    @property
    def uid(self) -> str | None:
        return self._uid

    @property
    def key(self) -> str:
        if self._key is None:
            raise ValueError("key is not set")
        return self._key

    @property
    def disable(self) -> bool:
        if self._disable is None:
            raise ValueError("disable is not set")
        return self._disable

    @property
    def value(self):
        return self._value

    def on_poolaccess_connect(self, client: PoolAccessClient):
        topic = client.build_topic(PoolAccessTopicMode.GET, self._uid)
        self._logger.info("Publishing to poolaccess: %s", topic)
        client.publish(topic)

    def on_poolaccess_message(self, client: PoolAccessClient, message: MQTTMessage):
        if message.topic == client.build_topic(PoolAccessTopicMode.VALUE, self._uid):
            self._logger.info("Reading %s %s", message.topic, str(message.payload))
            try:
                self._value = json.loads(message.payload)
            except JSONDecodeError as jde:
                self._logger.error(jde)
