#!/usr/bin/env python
import json

from .BayrolPoolaccessDevice import BayrolPoolaccessDevice
from .Sensor import Sensor

MESSAGES = {
    "8.5": {
        "message": "Pompe de filtration arrêtée",
        "type": "warning"
    },
    "8.6": {
        "message": "Pompe de filtration arrêtée\n(pas de signal 230V~ de la pompe de filtration)",
        "type": "warning"
    },
    "8.7": {
        "message": "Délai de démarrage",
        "type": "info"
    },
    "8.8": {
        "message": "Gaz détecté dans la cellule\n! Electrolyse de sel arrêtée !",
        "type": "warning"
    },
    "8.9": {
        "message": "Mesure redox trop basse depuis plusieurs jours\n! Electrolyse en mode \"Safe\" !",
        "type": "warning"
    },
    "8.10": {
        "message": "Mesure redox trop basse depuis plusieurs jours\n! Electrolyse arrêtée !",
        "type": "warning"
    },
    "8.11": {
        "message": "Mesure redox trop basse\ndepuis plusieurs jours",
        "type": "warning"
    },
    "8.12": {
        "message": "La mesure redox n'augmente pas comme prévu\n! Electrolyse en mode \"Safe\" !",
        "type": "warning"
    },
    "8.13": {
        "message": "La mesure redox n'augmente pas comme prévu\n! Electrolyse arrêtée !",
        "type": "warning"
    },
    "8.14": {
        "message": "La mesure redox n'augmente pas comme prévu",
        "type": "warning"
    },
    "8.15": {
        "message": "La mesure pH ne réagit pas comme prévu\n! Dosage pH arrêté !",
        "type": "warning"
    },
    "8.16": {
        "message": "La mesure redox ne réagit pas comme prévu\n! Dosage chlore arrêté !",
        "type": "warning"
    },
    "8.17": {
        "message": "Bidon de pH-Minus vide",
        "type": "warning"
    },
    "8.18": {
        "message": "Bidon de pH-Plus vide",
        "type": "warning"
    },
    "8.19": {
        "message": "Taux de sel trop bas\n! Electrolyse arrêtée !",
        "type": "warning"
    },
    "8.20": {
        "message": "Taux de sel trop faible\n! Production réduite (protection cellule)  !",
        "type": "warning"
    },
    "8.21": {
        "message": "Taux de sel inférieur au taux préféré",
        "type": "warning"
    },
    "8.22": {
        "message": "Production par électrolyse trop faible",
        "type": "warning"
    },
    "8.23": {
        "message": "Mesure pH trop haute",
        "type": "warning"
    },
    "8.24": {
        "message": "Mesure pH trop basse",
        "type": "warning"
    },
    "8.25": {
        "message": "Température de l'eau trop basse\nElectrolyse arrêtée",
        "type": "warning"
    },
    "8.26": {
        "message": "Température de l'eau basse\nElectrolyse arrêtée",
        "type": "warning"
    },
    "8.27": {
        "message": "Température de l'eau trop basse\nProduction réduite (protection cellule)",
        "type": "warning"
    },
    "8.28": {
        "message": "Mesure redox trop haute",
        "type": "warning"
    },
    "8.29": {
        "message": "Mesure redox trop basse",
        "type": "warning"
    },
    "8.30": {
        "message": "Pas de courant cellule",
        "type": "warning"
    },
    "8.31": {
        "message": "Temps de filtration journalier\npotentiellement trop faible",
        "type": "warning"
    },
    "8.32": {
        "message": "Bidon de Chloriliquide vide",
        "type": "warning"
    },
    "8.33": {
        "message": "Tout va bien. Profitez de votre piscine !",
        "type": "success"
    },
    "8.34": {
        "message": "Software reset",
        "type": "warning"
    },
    "8.35": {
        "message": "Power on",
        "type": "info"
    },
    "8.36": {
        "message": "Default reset",
        "type": "info"
    }
}


class MessagesSensor(Sensor):
    def __init__(self, data: dict, device: BayrolPoolaccessDevice, dicovery_prefix: str = "homeassistant"):
        super().__init__(data, device, dicovery_prefix)

    def build_payload(self, json_object):
        super().build_payload(json_object)
        # iterate through message strings
        if "v" in json_object:
            ar = json_object["v"]
            for i in range(len(ar)):
                if ar[i] in MESSAGES:
                    ar[i] = MESSAGES[ar[i]]
