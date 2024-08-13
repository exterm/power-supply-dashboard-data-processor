import logging
import os
from typing import Optional

import requests

ELECTRICITYMAPS_BASE_URL = "https://api.electricitymap.org/v3"

class Client:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_zones(self) -> dict:
        return self._make_request(f"{ELECTRICITYMAPS_BASE_URL}/zones")

    def get_carbon_intensity(self, zone: str) -> dict:
        return self._make_request(f"{ELECTRICITYMAPS_BASE_URL}/carbon-intensity/history?zone={zone}")

    def get_power_breakdown(self, zone: str) -> dict:
        return self._make_request(f"{ELECTRICITYMAPS_BASE_URL}/power-breakdown/history?zone={zone}")

    def _make_request(self, url: str) -> dict:
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
    response = client.get_carbon_intensity('FR')

    # response format: {'zone': 'FR', 'carbonIntensity': 19, 'datetime': '2024-08-11T21:00:00.000Z', 'updatedAt': '2024-08-11T21:47:37.609Z', 'createdAt': '2024-08-08T21:49:46.129Z', 'emissionFactorType': 'lifecycle', 'isEstimated': True, 'estimationMethod': 'TIME_SLICER_AVERAGE'}

    assert response["zone"] == "FR"
    print(response)
    first_entry = response["history"][0]
    assert isinstance(first_entry["carbonIntensity"], int)
    assert isinstance(first_entry["datetime"], str)
    assert isinstance(first_entry["updatedAt"], str)
    assert isinstance(first_entry["createdAt"], str)


def test_get_power_breakdown():
    client = Client()
    response = client.get_power_breakdown('FR')

    # response format: {'zone': 'FR', 'datetime': '2024-08-11T21:00:00.000Z', 'updatedAt': '2024-08-11T20:47:01.873Z', 'createdAt': '2024-08-08T21:49:46.129Z', 'powerConsumptionBreakdown': {'nuclear': 36253, 'geothermal': 0, 'biomass': 683, 'coal': 0, 'wind': 4128, 'solar': 0, 'hydro': 4730, 'gas': 546, 'oil': 104, 'unknown': 0, 'hydro discharge': 881, 'battery discharge': 0}, 'powerProductionBreakdown': {'nuclear': 42290, 'geothermal': None, 'biomass': 797, 'coal': 0, 'wind': 4815, 'solar': 0, 'hydro': 5518, 'gas': 637, 'oil': 122, 'unknown': None, 'hydro discharge': 1028, 'battery discharge': -7}, 'powerImportBreakdown': {'BE': 0, 'ES': 0, 'GB': 0}, 'powerExportBreakdown': {'BE': 2054, 'ES': 2468, 'GB': 3352}, 'fossilFreePercentage': 99, 'renewablePercentage': 22, 'powerConsumptionTotal': 47326, 'powerProductionTotal': 55207, 'powerImportTotal': 0, 'powerExportTotal': 7874, 'isEstimated': True, 'estimationMethod': 'TIME_SLICER_AVERAGE'}

    assert response["zone"] == "FR"
    first_entry = response["history"][0]
    assert isinstance(first_entry["powerConsumptionBreakdown"]["nuclear"], int)
    assert isinstance(first_entry["powerProductionBreakdown"]["nuclear"], int)
    assert isinstance(first_entry["powerImportBreakdown"]["BE"], int)
    assert isinstance(first_entry["powerExportBreakdown"]["BE"], int)
    assert isinstance(first_entry["fossilFreePercentage"], int)
    assert isinstance(first_entry["renewablePercentage"], int)
    assert isinstance(first_entry["powerConsumptionTotal"], int)


