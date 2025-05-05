#!/usr/bin/env python3
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Light(Entity):
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, dicovery_prefix: str = "homeassistant"):
        super().__init__(data, device, dicovery_prefix)
        data["payload_on"] = "on"
        data["payload_off"] = "off"
        if "command_topic" not in data:
            data["command_topic"] = "%s/set" % data["state_topic"]

    @property
    def type(self) -> str:
        return "light"

    @property
    def command_topic(self) -> str:
        return self._attributes["command_topic"]

    def build_config(self):
        return super().build_config()
