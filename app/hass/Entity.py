import re
import json
from datetime import datetime

from .BayrolPoolaccessDevice import BayrolPoolaccessDevice


def norm(s: str):
    s = re.sub(u"[\W|_]", "", s)
    return s.lower()


def load_attr(key: str, data: dict):
    assert key in data
    value = data[key]
    del data[key]
    return value


class Entity:
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, discovery_prefix: str = "homeassistant"):
        self._uid = load_attr("uid", data)
        self._key = load_attr("key", data)
        self._attributes = data
        self._device = device
        self._discovery_prefix = discovery_prefix

        # config variables
        self._attributes["unique_id"] = ("%s_%s_%s" % (norm(device.manufacturer), norm(self._device.id),self.key))
        self._attributes["state_topic"] = "%s/%s/%s/%s" % (discovery_prefix, self.type, device.id, self.key)

        if "name" not in data:
            self._attributes["name"] = self._key

        if "availability" not in data:
            self._attributes["availability"] = [{
                "topic": "%s/sensor/%s/status" % (discovery_prefix, device.id),
                "value_template": "{{ 'online' if value_json.v | float > 17.0 else 'offline' }}"
            }]

        if "value_template" not in data:
            self._attributes["value_template"] = "{{ value_json.v }}"

        if "json_attributes_topic" not in data and "json_attributes_template" in data:
            self._attributes["json_attributes_topic"] = self.state_topic

    @property
    def uid(self) -> str:
        return self._uid

    @property
    def key(self) -> str:
        return self._key

    @property
    def name(self) -> str:
        return self._attributes["name"]

    @property
    def state_topic(self) -> str:
        return self._attributes["state_topic"]

    @property
    def type(self) -> str:
        raise NotImplementedError

    def get_payload(self, message: bytes = None):
        if message is None:
            return None
        json_object = json.loads(message)
        self.build_payload(json_object)
        return json.dumps(json_object)

    def build_payload(self, json_object):
        json_object["updatedAt"] = f"{datetime.utcnow().isoformat()[:-3]}Z"

    def build_config(self):
        return "%s/config" % self.state_topic, { **self._attributes, "device": self._device }
