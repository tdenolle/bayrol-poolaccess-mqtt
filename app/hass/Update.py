#!/usr/bin/env python3
import logging
import os

import requests

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity


class Update(Entity):
    ENTITY_PLATFORM = "update"
    DEFAULT_BAYROL_SUPPORT_URL = "https://www.bayrol.fr/bayrol-technik-support"
    
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, discovery_prefix: str = "homeassistant"):
        super().__init__(data, device, discovery_prefix)
        self._attributes["platform"] = self.ENTITY_PLATFORM

        update_data = self._get_update_data(device)

        self._attributes["value_template"] = ("{ \"installed_version\": \"{{ value_json.v }}\","
                                              "\"latest_version\": \"%s\","
                                              "\"release_url\": \"%s\" }" %
                                              (update_data.get("version", "unavailable"),
                                               update_data.get("url", self.DEFAULT_BAYROL_SUPPORT_URL)))

    @property
    def type(self) -> str:
        return self.ENTITY_PLATFORM

    def _get_update_data(self, device: BayrolPoolaccessDevice):
        try:
            update_version_endpoint = os.environ.get('UPDATE_VERSION_ENDPOINT')
            if not update_version_endpoint:
                self._logger.warning("[Update] UPDATE_VERSION_ENDPOINT environment variable is not set.")
                return {}
            response = requests.get(update_version_endpoint.format(id=device.id),
                                    headers={"User-Agent": f"BayrolPoolaccess/{os.environ.get('APP_VERSION', '0.0.0')}"},
                                    timeout=5,
                                    allow_redirects=False)
            self._logger.debug(f"[Update] Fetched update data from {update_version_endpoint} with status code {response.status_code}")
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
             self._logger.error(f"[Update] RequestException fetching update data: {e}")
        except ValueError  as e:
             self._logger.error(f"[Update] ValueError fetching update data: {e}")
        return {}
