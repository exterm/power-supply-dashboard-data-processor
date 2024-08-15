def process(carbon_intensity: dict, power_breakdown: dict) -> dict:
    """
    Process the raw data from the Electricity Map API into a format that can be used by the dashboard.

    Args:
    carbon_intensity (dict): The raw carbon intensity history (24h) data from the Electricity Map API.
    power_breakdown (dict): The raw power breakdown history (24h) data from the Electricity Map API.

    Returns:
    dict: The processed data that can be used by the dashboard.
    """

    latest_carbon_intensity = carbon_intensity['history'][0]['carbonIntensity']
    latest_power_breakdown = power_breakdown['history'][0]

    average_carbon_intensity = sum(entry['carbonIntensity'] for entry in carbon_intensity['history'])
    average_carbon_intensity /= len(carbon_intensity['history'])

    processed_data = {
        'latest_carbon_intensity': latest_carbon_intensity,
        'average_carbon_intensity': average_carbon_intensity,
        'percent_carbon_free': latest_power_breakdown['fossilFreePercentage'],
    }

    return processed_data

def test_process():
    carbon_intensity = {
        "zone": "FR",
        "history": [
            {
                "carbonIntensity": 50,
                "datetime": "2021-10-01T00:00:00Z",
                "updatedAt": "2021-10-01T00:00:00Z",
                "createdAt": "2021-10-01T00:00:00Z"
            },
            {
                "carbonIntensity": 100,
                "datetime": "2021-10-01T01:00:00Z",
                "updatedAt": "2021-10-01T01:00:00Z",
                "createdAt": "2021-10-01T01:00:00Z"
            }
        ]
    }

    power_breakdown = {
        "zone": "FR",
        "history": [
            {
                "powerConsumptionBreakdown": {
                    "nuclear": 1000
                },
                "powerProductionBreakdown": {
                    "nuclear": 2000
                },
                "powerImportBreakdown": {
                    "BE": 500
                },
                "powerExportBreakdown": {
                    "BE": 100
                },
                "fossilFreePercentage": 50,
                "renewablePercentage": 30,
                "powerConsumptionTotal": 5000
            }
        ]
    }

    processed_data = process(carbon_intensity, power_breakdown)

    assert processed_data['latest_carbon_intensity'] == 50
    assert processed_data['average_carbon_intensity'] == 75
    assert processed_data['percent_carbon_free'] == 50
