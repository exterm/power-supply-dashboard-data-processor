import os

import flask
import functions_framework

import supabase

SUPABASE_URL = 'https://zsfmcbykdoviifsoauxs.supabase.co'
SUPABASE_TOKEN = os.getenv('SUPABASE_TOKEN')

@functions_framework.http
def main(request: flask.Request) -> flask.typing.ResponseReturnValue:
    db: supabase.Client = supabase.create_client(SUPABASE_URL, SUPABASE_TOKEN)

    response = db.table('dashboard-snapshots').select("*").execute()

    print(response.json())

    response = db.table('dashboard-snapshots').insert({
      'region': 'Ontario',
      'data': {"carbon_free_share": 0.5},
    }).execute()
    return response.json()
