import logging

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
    response = client.get_carbon_intensity("FR")

    assert response["zone"] == "FR"
    print(response)
    first_entry = response["history"][0]
    assert isinstance(first_entry["carbonIntensity"], int)
    assert isinstance(first_entry["datetime"], str)
    assert isinstance(first_entry["updatedAt"], str)
    assert isinstance(first_entry["createdAt"], str)


def test_get_power_breakdown():
    client = Client()
    response = client.get_power_breakdown("FR")

    assert response["zone"] == "FR"
    first_entry = response["history"][0]
    assert isinstance(first_entry["powerConsumptionBreakdown"]["nuclear"], int)
    assert isinstance(first_entry["powerProductionBreakdown"]["nuclear"], int)
    assert isinstance(first_entry["powerImportBreakdown"]["BE"], int)
    assert isinstance(first_entry["powerExportBreakdown"]["BE"], int)
    assert isinstance(first_entry["fossilFreePercentage"], int)
    assert isinstance(first_entry["renewablePercentage"], int)
    assert isinstance(first_entry["powerConsumptionTotal"], int)
