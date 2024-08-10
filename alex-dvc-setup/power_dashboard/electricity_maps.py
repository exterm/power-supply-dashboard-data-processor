import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)

ELECTRICITYMAPS_BASE_URL = "https://api.electricitymap.org/v3/"


def get_electricity_maps_zones():
    url = f"{ELECTRICITYMAPS_BASE_URL}zones"

    # Send the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Request failed with status code: {response.status_code}")
        raise requests.exceptions.HTTPError("Response: " + response.text)


def get_electricity_maps_carbon_intensity(
    lat: float, lng: float, auth_token: Optional[str] = None
):
    url = f"{ELECTRICITYMAPS_BASE_URL}carbon-intensity/history?lat={lat}&lon={lng}"

    if auth_token is None:
        auth_token = os.getenv("ELECTRICITYMAPS_API_KEY")

    # Define the headers with the auth token
    headers = {"auth-token": auth_token}

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Request failed with status code: {response.status_code}")
        raise requests.exceptions.HTTPError("Response: " + response.text)


def get_electricity_maps_power_breakdown(
    lat: float, lng: float, auth_token: Optional[str] = None
):
    url = f"{ELECTRICITYMAPS_BASE_URL}power-breakdown/latest?lat={lat}&lon={lng}"

    if auth_token is None:
        auth_token = os.getenv("ELECTRICITYMAPS_API_KEY")

    # Define the headers with the auth token
    headers = {"auth-token": auth_token}

    # Send the GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Request failed with status code: {response.status_code}")
        raise requests.exceptions.HTTPError("Response: " + response.text)
