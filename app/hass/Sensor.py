#!/usr/bin/env python3

from app.hass.Entity import Entity, normalize


class Sensor(Entity):

    def __init__(self, data: dict):
        super().__init__(data)

    @property
    def type(self) -> str:
        return "sensor"


