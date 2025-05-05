#!/usr/bin/env python3
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Climate(Entity):
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, dicovery_prefix: str = "homeassistant"):
        super().__init__(data, device, dicovery_prefix)

        if "config_topic" not in data:
            data["config_topic"] = "%s/config" % data["state_topic"]
        
    @property
    def type(self) -> str:
        return "climate"

    @property
    def config_topic(self) -> str:
        return self._attributes["config_topic"]

    def build_config(self):
        return super().build_config()
