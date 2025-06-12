import re

BAYROL_MANUFACTURER_NAME = "Bayrol"


def get_device_model_from_serial(device_serial: str):
    if re.match("[0-9]{2}ASE[0-9]-[0-9]{5}", device_serial):
        return "ASE","Automatic Salt"
    elif re.match("[0-9]{2}ACL[0-9]-[0-9]{5}", device_serial):
        return "ACL","Automatic Cl-pH"
    elif re.match("[0-9]{2}APH[0-9]-[0-9]{5}", device_serial):
        return "APH","Automatic pH"
    else:
        return "Unknown","Unknown"


class BayrolPoolaccessDevice(dict):

    def __init__(self, serial: str):
        super().__init__()
        self["identifiers"] = [serial]
        self["manufacturer"] = BAYROL_MANUFACTURER_NAME
        code,model = get_device_model_from_serial(serial)
        self["model"] = model
        self._code = code
        self["name"] = "%s %s" % (BAYROL_MANUFACTURER_NAME, serial)

    @property
    def id(self) -> str:
        return self["identifiers"][0]

    @property
    def manufacturer(self) -> str:
        return BAYROL_MANUFACTURER_NAME

    @property
    def model(self) -> str:
        return self["model"]

    @property
    def code(self) -> str:
        return self._code
