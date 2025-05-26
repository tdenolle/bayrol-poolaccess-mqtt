#!/usr/bin/env python3
import logging

import requests

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Update(Entity):
    ENTITY_PLATFORM = "update"
    BAYROL_UPDATE_URL = "https://www.denolle.fr/bayrol/update.json"
    BAYROL_SUPPORT_URL = "https://www.bayrol.fr/bayrol-technik-support"

    def __init__(self, data: dict, device: BayrolPoolaccessDevice, discovery_prefix: str = "homeassistant"):
        super().__init__(data, device, discovery_prefix)
        self._attributes["platform"] = self.ENTITY_PLATFORM

        update_data = self._get_update_data(device)

        self._attributes["value_template"] = ("{ \"installed_version\": \"{{ value_json.v }}\","
                                              "\"latest_version\": \"%s\","
                                              "\"release_url\": \"%s\" }" %
                                              (update_data.get("version", "{{ value_json.v }}"),
                                               update_data.get("url", self.BAYROL_SUPPORT_URL)))

    @property
    def type(self) -> str:
        return self.ENTITY_PLATFORM

    def _get_update_data(self, device: BayrolPoolaccessDevice):
        try:
            response = requests.get(self.BAYROL_UPDATE_URL,
                                    params={"id": device.id},
                                    timeout=5,
                                    allow_redirects=False)
            if response.status_code == 200:
                data = response.json()
                return data.get(device.model, {})
        except requests.RequestException as e:
            logging.getLogger().debug(f"Error fetching update data: {e}")
        return {}
