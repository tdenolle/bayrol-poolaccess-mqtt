#!/usr/bin/env python3
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Update(Entity):
    ENTITY_PLATFORM = "update"

    def __init__(self, data: dict, device: BayrolPoolaccessDevice, dicovery_prefix: str = "homeassistant"):
        super().__init__(data, device, dicovery_prefix)
        self._attributes["platform"] = self.ENTITY_PLATFORM

    @property
    def type(self) -> str:
        return self.ENTITY_PLATFORM
