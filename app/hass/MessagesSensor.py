#!/usr/bin/env python
import copy

from app.hass.BayrolPoolaccessDevice import BayrolPoolaccessDevice
from app.hass.Sensor import Sensor

MESSAGES = {"8.5": {"key": "al_no_flow_bnc", "type": "warning"},
            "8.6": {"key": "al_no_flow_230V", "type": "warning"},
            "8.7": {"key": "al_start_delay", "type": "info"},
            "8.8": {"key": "al_se_gas_detected", "type": "warning"},
            "8.9": {"key": "al_se_err_setpoint_safe_mode", "type": "warning"},
            "8.10": {"key": "al_se_err_setpoint_stopped", "type": "warning"},
            "8.11": {"key": "al_se_err_setpoint", "type": "warning"},
            "8.12": {"key": "al_se_err_rise_safe_mode", "type": "warning"},
            "8.13": {"key": "al_se_err_rise_stopped", "type": "warning"},
            "8.14": {"key": "al_se_err_rise", "type": "warning"},
            "8.15": {"key": "al_ph_dosing_stopped", "type": "warning"},
            "8.16": {"key": "al_mv_dosing_stopped","type": "warning"},
            "8.17": {"key": "al_ph_minus_empty", "type": "warning"},
            "8.18": {"key": "al_ph_plus_empty", "type": "warning"},
            "8.19": {"key": "al_salt_low_stopped", "type": "warning"},
            "8.20": {"key": "al_salt_low_cell_protection","type": "warning"},
            "8.21": {"key": "al_salt_low_pre_warning", "type": "warning"},
            "8.22": {"key": "al_se_production_low", "type": "warning"},
            "8.23": {"key": "al_ph_too_high", "type": "warning"},
            "8.24": {"key": "al_ph_too_low","type": "warning"},
            "8.25": {"key": "al_se_t_low_stopped", "type": "warning"},
            "8.26": {"key": "al_se_t_low_stopped_user", "type": "warning"},
            "8.27": {"key": "al_se_t_low_cell_protection", "type": "warning"},
            "8.28": {"key": "al_mv_too_high","type": "warning"},
            "8.29": {"key": "al_mv_too_low", "type": "warning"},
            "8.30": {"key": "al_se_no_current", "type": "warning"},
            "8.31": {"key": "al_filtration_short", "type": "warning"},
            "8.32": {"key": "al_cl_empty","type": "warning"},
            "8.33": {"key": "enjoy", "type": "success"},
            "8.34": {"key": "ev_sw_reset", "type": "warning"},
            "8.35": {"key": "ev_system_start", "type": "info"},
            "8.36": {"key": "ev_default_reset", "type": "info"}}


class MessagesSensor(Sensor):
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, discovery_prefix: str = "homeassistant"):
        super().__init__(data, device, discovery_prefix)
        # Build Messages array
        self._messages = copy.deepcopy(MESSAGES)
        for uid in self._messages:
            m = self._messages[uid]
            k = m["key"]
            m["message"] = self._lang.get_string(k,k)

    def build_payload(self, json_object):
        super().build_payload(json_object)
        # iterate through message strings
        if "v" in json_object:
            ar = json_object["v"]
            for i in range(len(ar)):
                if ar[i] in self._messages:
                    ar[i] = self._messages[ar[i]]
