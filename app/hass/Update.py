#!/usr/bin/env python3
import requests

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Update(Entity):
    ENTITY_PLATFORM = "update"
    BAYROL_UPDATE_URL = "https://www.denolle.fr/bayrol/update.json"

    def __init__(self, data: dict, device: BayrolPoolaccessDevice, dicovery_prefix: str = "homeassistant"):
        super().__init__(data, device, dicovery_prefix)
        self._attributes["platform"] = self.ENTITY_PLATFORM

        update_data = self._get_update_data(device)

        if "value_template" not in data:
            self._attributes["value_template"] = ("{ \"installed_version\": \"{{ value_json.v }}\","
                                                  "\"latest_version\": \"%s\","
                                                  "\"title\": \"Bayrol Firmware\","
                                                  "\"release_url\": \"%s\","
                                                  "\"release_summary\": \"A new version of Bayrol firmware\","
                                                  "\"entity_picture\": null }" %
                                                  (update_data.get("version", "{{ value_json.v }}"),
                                                   update_data.get("url", "")))

    @property
    def type(self) -> str:
        return self.ENTITY_PLATFORM

    def _get_update_data(self, device: BayrolPoolaccessDevice):
        response = requests.get(self.BAYROL_UPDATE_URL,
                                params={"id": device.id},
                                timeout=5,
                                allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            return data.get(device.model, {})
        return {}
