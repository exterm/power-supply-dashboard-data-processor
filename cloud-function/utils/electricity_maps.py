import logging
import os
from typing import Optional

import requests

ELECTRICITYMAPS_BASE_URL = "https://api.electricitymap.org/v3"

class Client:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_zones(self):
        return self._make_request(f"{ELECTRICITYMAPS_BASE_URL}/zones")

    def get_carbon_intensity(self, lat: float, lng: float):
        return self._make_request(f"{ELECTRICITYMAPS_BASE_URL}/carbon-intensity/latest?lat={lat}&lon={lng}")

    def get_power_breakdown(self, lat: float, lng: float):
        return self._make_request(f"{ELECTRICITYMAPS_BASE_URL}/power-breakdown/latest?lat={lat}&lon={lng}")

    def _make_request(self, url: str):
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"Request failed with status code: {response.status_code}")
            raise requests.exceptions.HTTPError("Response: " + response.text)

# tests

def test_get_zones():
    client = Client()
    response = client.get_zones()

    assert response["AD"]["zoneName"] == "Andorra"

def test_get_carbon_intensity():
    client = Client()
    response = client.get_carbon_intensity(43.6, 1.44)

    # response format: {'zone': 'FR', 'history': [{'zone': 'FR', 'carbonIntensity': 20, 'datetime': '2024-08-10T22:00:00.000Z', 'updatedAt': '2024-08-11T06:48:10.211Z', 'createdAt': '2024-08-07T22:50:30.774Z', 'emissionFactorType': 'lifecycle', 'isEstimated': False, 'estimationMethod': None}, ...]}

    assert response["zone"] == "FR"
    assert response["history"][0]["zone"] == "FR"
    assert isinstance(response["history"][0]["carbonIntensity"], int)

def test_get_power_breakdown():
    client = Client()
    response = client.get_power_breakdown(43.6, 1.44)

    # response format: {'zone': 'FR', 'datetime': '2024-08-11T21:00:00.000Z', 'updatedAt': '2024-08-11T20:47:01.873Z', 'createdAt': '2024-08-08T21:49:46.129Z', 'powerConsumptionBreakdown': {'nuclear': 36253, 'geothermal': 0, 'biomass': 683, 'coal': 0, 'wind': 4128, 'solar': 0, 'hydro': 4730, 'gas': 546, 'oil': 104, 'unknown': 0, 'hydro discharge': 881, 'battery discharge': 0}, 'powerProductionBreakdown': {'nuclear': 42290, 'geothermal': None, 'biomass': 797, 'coal': 0, 'wind': 4815, 'solar': 0, 'hydro': 5518, 'gas': 637, 'oil': 122, 'unknown': None, 'hydro discharge': 1028, 'battery discharge': -7}, 'powerImportBreakdown': {'BE': 0, 'ES': 0, 'GB': 0}, 'powerExportBreakdown': {'BE': 2054, 'ES': 2468, 'GB': 3352}, 'fossilFreePercentage': 99, 'renewablePercentage': 22, 'powerConsumptionTotal': 47326, 'powerProductionTotal': 55207, 'powerImportTotal': 0, 'powerExportTotal': 7874, 'isEstimated': True, 'estimationMethod': 'TIME_SLICER_AVERAGE'}

    assert response["zone"] == "FR"
    assert isinstance(response["powerConsumptionBreakdown"]["nuclear"], int)
    assert isinstance(response["powerProductionBreakdown"]["nuclear"], int)
    assert isinstance(response["powerImportBreakdown"]["BE"], int)
    assert isinstance(response["powerExportBreakdown"]["BE"], int)
    assert isinstance(response["fossilFreePercentage"], int)
    assert isinstance(response["renewablePercentage"], int)
    assert isinstance(response["powerConsumptionTotal"], int)


