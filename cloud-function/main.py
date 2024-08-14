import os

import flask
import functions_framework

import supabase

from utils import electricity_maps
from utils import dashboard_processing

SUPABASE_URL = 'https://zsfmcbykdoviifsoauxs.supabase.co'
SUPABASE_TOKEN = os.getenv('SUPABASE_TOKEN')

@functions_framework.http
def main(request: flask.Request) -> flask.typing.ResponseReturnValue:
  db: supabase.Client = supabase.create_client(SUPABASE_URL, SUPABASE_TOKEN)

  electricity_maps_client = electricity_maps.Client()

  interesting_zones = ['CA-ON', 'US-NE-ISNE', 'US-NW-WACM']

  for zone in interesting_zones:
    carbon_intensity = electricity_maps_client.get_carbon_intensity(zone)
    power_breakdown = electricity_maps_client.get_power_breakdown(zone)
    db.table('electricitymaps-hourly').insert({
      'zone': zone,
      'carbon_intensity_raw': carbon_intensity,
      'power_breakdown_raw': power_breakdown,
      'testing': not is_running_in_gcp()
    }).execute()

    if zone == 'CA-ON':
      dashboard_data = dashboard_processing.process(carbon_intensity, power_breakdown)
      db.table('dashboard-snapshots').insert({
        'zone': zone,
        'data': dashboard_data,
        'testing': not is_running_in_gcp()
      }).execute()

  return 'OK'

def is_running_in_gcp():
    return os.getenv('K_SERVICE') is not None
