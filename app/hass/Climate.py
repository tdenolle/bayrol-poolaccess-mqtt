#!/usr/bin/env python3
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Climate(Entity):
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, dicovery_prefix: str = "homeassistant"):
        super().__init__(data, device, dicovery_prefix)
        

    @property
    def type(self) -> str:
        return "climate"

    @property
    def command_topic(self) -> str:
        return self._attributes["command_topic"]

    def build_config(self):
        return super().build_config()
