#!/usr/bin/env python3

import re


class Sensor:
    def __init__(self, data: dict):
        self._uid = load_attr("uid", data)
        self._key = load_attr("key", data)
        self._name = load_attr("name", data)
        self._attributes = data

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> str:
        return self._name

    @property
    def attributes(self) -> dict:
        return self._attributes

    def get_payload(self, message: bytes = None) -> bytes:
        return message

    def build_config(self, device: dict, hass_dicovery_prefix: str = "homeassistant"):
        # variables
        device_id = str(device["identifiers"][0])
        sensor_topic_prefix = "%s/sensor/%s" % (hass_dicovery_prefix, device_id)
        state_topic = "%s/%s" % (sensor_topic_prefix, self.key)
        # config build-ins
        config = self.attributes
        config["unique_id"] = ("bayrol_%s_%s" % (normalize(device_id), self.key))
        config["name"] = self.name
        config["state_topic"] = state_topic
        config["availability"] = [{
            "topic": "%s/status" % sensor_topic_prefix,
            "value_template": "{{ 'online' if value_json.v | float > 17.0 else 'offline' }}"
        }]
        if "value_template" not in config:
            config["value_template"] = "{{ value_json.v }}"
        config["device"] = device
        if "json_attributes_topic" not in config and "json_attributes_template" in config:
            config["json_attributes_topic"] = state_topic
        return "%s/config" % state_topic, config


def normalize(s: str):
    s = re.sub(u"[\W|_]", "", s)
    return s.lower()


def load_attr(key: str, data: dict):
    assert key in data
    value = data[key]
    del data[key]
    return value
