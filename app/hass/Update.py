#!/usr/bin/env python3
import json
import logging
import os

import requests

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Entity import Entity
from app.mqtt.MqttClient import MqttClient
from app.mqtt.PoolAccessClient import PoolAccessClient


class Update(Entity):
    ENTITY_PLATFORM = "update"
    DEFAULT_BAYROL_SUPPORT_URL = "https://www.bayrol.fr/bayrol-technik-support"
    
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, discovery_prefix: str = "homeassistant"):
        super().__init__(data, device, discovery_prefix)
        self._attributes["platform"] = self.ENTITY_PLATFORM
        self._update_value_template()

    @property
    def type(self) -> str:
        return self.ENTITY_PLATFORM

    def on_periodic_refresh(self, poolaccess_client: PoolAccessClient, broker_client: MqttClient):
        """Re-fetch update data and republish config + trigger GET."""
        self._logger.info("[Update] Periodic refresh for sw_version")
        self._update_value_template()
        # Republish config to broker
        (topic, cfg) = self.build_config()
        payload = str(json.dumps(cfg))
        self._logger.info("[Update] Refreshing config: %s", topic)
        broker_client.publish(topic, payload=payload, retain=True)
        # Trigger GET to poolaccess for installed version
        self.on_poolaccess_connect(poolaccess_client)

    def _update_value_template(self):
        update_data = self._get_update_data(self._device)
        self._attributes["value_template"] = ("{ \"installed_version\": \"{{ value_json.v }}\","
                                              "\"latest_version\": \"%s\","
                                              "\"release_url\": \"%s\" }" %
                                              (update_data.get("version", "unavailable"),
                                               update_data.get("url", self.DEFAULT_BAYROL_SUPPORT_URL)))

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
