import datetime
import os

import flask
import functions_framework

import supabase

from utils import electricity_maps, hydro_ottawa, dashboard

SUPABASE_URL = "https://zsfmcbykdoviifsoauxs.supabase.co"
SUPABASE_TOKEN = os.getenv("SUPABASE_TOKEN")
PHILIP_UTILITY_USERNAME = os.getenv("PHILIP_UTILITY_USERNAME")
PHILIP_UTILITY_PASSWORD = os.getenv("PHILIP_UTILITY_PASSWORD")
ELECTRICITYMAPS_TOKEN = os.getenv("ELECTRICITYMAPS_TOKEN")
if not SUPABASE_TOKEN or not PHILIP_UTILITY_USERNAME or not PHILIP_UTILITY_PASSWORD or not ELECTRICITYMAPS_TOKEN:
  raise Exception(
    "SUPABASE_TOKEN, PHILIP_UTILITY_USERNAME, PHILIP_UTILITY_PASSWORD, and ELECTRICITYMAPS_TOKEN must be set as environment variables"
  )


@functions_framework.http
def main(request: flask.Request) -> flask.typing.ResponseReturnValue:
  db: supabase.Client = supabase.create_client(SUPABASE_URL, SUPABASE_TOKEN)

  electricity_maps_client = electricity_maps.Client(ELECTRICITYMAPS_TOKEN)

  interesting_zones = ["CA-ON", "US-NE-ISNE", "US-NW-WACM"]

  db.table("electricitymaps-hourly").delete().gte("created_at", datetime.datetime.now(datetime.UTC) - datetime.timedelta(months=2)).execute()
  for zone in interesting_zones:
    carbon_intensity = electricity_maps_client.get_carbon_intensity(zone)
    power_breakdown = electricity_maps_client.get_power_breakdown(zone)
    db.table("electricitymaps-hourly").insert(
      {
        "zone": zone,
        "carbon_intensity_raw": carbon_intensity,
        "power_breakdown_raw": power_breakdown,
        "testing": not is_running_in_gcp(),
      }
    ).execute()

    dashboard.precalculate(db, zone, not is_running_in_gcp())

  philip_utility_client = hydro_ottawa.Client(PHILIP_UTILITY_USERNAME, PHILIP_UTILITY_PASSWORD)

  db.table("private-utility-datapoints").delete().gte("created_at", datetime.datetime.now(datetime.UTC) - datetime.timedelta(months=2)).execute()
  db.table("private-utility-datapoints").insert(
    {"household": "Philip's Place", "data": philip_utility_client.get_data(), "testing": not is_running_in_gcp()}
  ).execute()


  return "OK"


def is_running_in_gcp() -> bool:
  return os.getenv("K_SERVICE") is not None
