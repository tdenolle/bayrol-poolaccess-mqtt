#!/usr/bin/env python3

from app.hass.Entity import Entity


class Switch(Entity):
    def __init__(self, data: dict):
        super().__init__(data)
        data["payload_on"] = "on"
        data["payload_off"] = "off"

    @property
    def type(self) -> str:
        return "switch"

    def build_config(self, device: dict, hass_dicovery_prefix: str = "homeassistant"):
        (topic, cfg) = super().build_config(device, hass_dicovery_prefix)
        cfg["command_topic"] = "%s/set" % cfg["state_topic"]
        return topic, cfg
