import re
import json

from app.Utils import normalize_string


class Sensor:
    def __init__(self, data: dict):
        self._uid = load_attr("uid", data)
        self._name = load_attr("name", data)
        self._attributes = data

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def name(self) -> str:
        return self._name

    @property
    def attributes(self) -> dict:
        return self._attributes

    @property
    def payload(self):
        return None

    def build_config(self, device: dict, hass_dicovery_prefix: str = "homeassistant"):
        # variables
        device_id = str(device["identifiers"][0])
        normalized_name = normalize_string(self.name, "_")
        sensor_topic_prefix = "%s/sensor/%s" % (hass_dicovery_prefix, device_id)
        config_topic = "%s/%s/config" % (sensor_topic_prefix, normalized_name)
        # config build-ins
        config = self.attributes
        config["unique_id"] = ("bayrol_%s_%s" % (normalize_string(device_id, ""), normalized_name))
        config["name"] = self.name
        config["state_topic"] = "%s/%s" % (sensor_topic_prefix, normalized_name)
        config["availability"] = [{
            "topic": "%s/status" % sensor_topic_prefix,
            "value_template": "{{ 'online' if value_json.v | float > 17.0 else 'offline' }}"
        }]
        if "value_template" not in config:
            config["value_template"] = "{{ value_json.v }}"
        config["device"] = device
        config["json_attributes_topic"] = config["state_topic"]
        return config_topic, config


def load_attr(key: str, data: dict):
    assert key in data
    value = data[key]
    del data[key]
    return value


def load_sensors(filepath: str) -> list[Sensor]:
    with open(filepath, 'r') as f:
        return [Sensor(s) for s in json.load(f)]
