#!/usr/bin/env python3
from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Climate(Entity):
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, dicovery_prefix: str = "homeassistant"):
        super().__init__(data, device, dicovery_prefix)
        self._uid_mode = data['uid_mode']
        self._uid_temp = data['_uid_temp']

        if "temperature_command_topic" not in data:
            data["temperature_command_topic"] = "%s/set_temp" % data["state_topic"]

        if "mode_command_topic" not in data:
            data["mode_command_topic"] = "%s/set_mode" % data["state_topic"]
        
    @property
    def type(self) -> str:
        return "climate"

    @property
    def uid_mode(self) -> str:
        return self._uid_mode

    @property
    def uid_temp(self) -> str:
        return self._uid_temp

    @property
    def temperature_command_topic(self) -> str:
        return self._attributes["temperature_command_topic"]

    @property
    def mode_command_topic(self) -> str:
        return self._attributes["mode_command_topic"]

    def build_config(self):
        return super().build_config()
