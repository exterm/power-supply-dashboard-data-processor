import supabase
import datetime

def precalculate(db: supabase.Client, zone: str, testing: bool):
    # fetch data for the last 7 days (UTC) of carbon intensity from the supabase database
    # each row in the table has a UTC created_at timestamp
    seven_days_ago = datetime.datetime.now(datetime.UTC) - datetime.timedelta(days=7)
    response = db.table("electricitymaps-hourly").select("carbon_intensity_raw,power_breakdown_raw,created_at")\
      .eq("zone", zone).gte("created_at", seven_days_ago).neq("testing", True).order("created_at", desc=False).execute()

    data = response.data

    db.table("dashboard-snapshots").insert(
      {
        "zone": zone,
        "data": {
            "carbon_intensity_history": extract_history(data, "carbon_intensity_raw", "carbonIntensity"),
            "power_breakdown_history": extract_history(data, "power_breakdown_raw", "powerConsumptionTotal"),
        },
        "testing": testing,
      }
    ).execute()

def extract_history(data, column, key):
    # Filter out duplicate rows for each hour and build the 7-day history
    history = []



    for row in data:
        history.append(row[column]["history"][0])

    # add newest 23 hours of the latest row
    latest_row = data[-1]

    for value in latest_row[column]["history"][1:]:
        history.append(value)

    # Extract numeric values from the raw data
    history = [datapoint[key] for datapoint in history]

    return history

# tests

def test_extract_carbon_intensity_history():
    data = [
        {
            "created_at": "2021-10-01T00:00:00.000000+00:00",
            "carbon_intensity_raw": {
                "history": [
                    {"carbonIntensity": 100},
                    {"carbonIntensity": 200},
                ]
            }
        },
        {
            "created_at": "2021-10-01T01:00:00.000000+00:00",
            "carbon_intensity_raw": {
                "history": [
                    {"carbonIntensity": 300},
                    {"carbonIntensity": 400},
                ]
            }
        }
    ]

    result = extract_history(data, "carbon_intensity_raw", "carbonIntensity")

    assert result == [100, 300, 400]
