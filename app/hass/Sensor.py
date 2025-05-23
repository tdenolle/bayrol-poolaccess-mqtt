#!/usr/bin/env python3
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Sensor(Entity):

    def __init__(self, data: dict, device: BayrolPoolaccessDevice, discovery_prefix: str = "homeassistant"):
        super().__init__(data, device, discovery_prefix)

    @property
    def type(self) -> str:
        return "sensor"


