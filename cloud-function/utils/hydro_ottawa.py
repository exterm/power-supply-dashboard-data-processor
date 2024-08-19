import requests
from pycognito import Cognito

# AWS Cognito configuration
client_id = "7scfcis6ecucktmp4aqi1jk6cb"
user_pool_id = "ca-central-1_VYnwOhMBK"


class Client:
  def __init__(self, username, password):
    self.username = username
    self.password = password

  def get_data(self):
    # Step 1: Authenticate and get tokens using pycognito
    u = Cognito(user_pool_id, client_id, username=self.username)
    u.authenticate(password=self.password)

    id_token = u.id_token
    access_token = u.access_token

    # Step 2: Use the tokens to get the loggedInAppToken from the response header
    app_token_url = "https://api-myaccount.hydroottawa.com/app-token"

    headers = {
      "x-id": id_token,
      "x-access": access_token,
      "Accept": "application/json",
    }

    # Step 3: Make the request to get the loggedInAppToken from the response headers
    response = requests.get(app_token_url, headers=headers)

    if response.status_code == 200:
      loggedInAppToken = response.headers.get("x-amzn-remapped-authorization")
    else:
      raise Exception(f"Failed to obtain loggedInAppToken: {response.status_code}\n{response.text}")

    # Step 4: Use the loggedInAppToken to make authenticated requests to the Hydro Ottawa API
    headers["Authorization"] = loggedInAppToken

    # first, get current billing period
    billing_period_url = "https://api-myaccount.hydroottawa.com/usage/billing-period-list"

    response = requests.get(billing_period_url, headers=headers)

    if response.status_code == 200:
      billing_periods = response.json()
      current_billing_period = billing_periods[0]
      start_date = current_billing_period["startDate"]
      end_date = current_billing_period["endDate"]
    else:
      raise Exception(f"Failed to obtain billing period: {response.status_code}\n{response.text}")

    # second, get usage data for the current billing period
    usage_url = "https://api-myaccount.hydroottawa.com/usage/consumption/billing-period"

    request_body = {"startDate": start_date, "endDate": end_date}

    response = requests.post(usage_url, headers=headers, json=request_body)

    if response.status_code == 200:
      usage_data = response.json()
      total_usage = usage_data["summary"]["totalUsage"]
    else:
      raise Exception(f"Failed to obtain usage data: {response.status_code}\n{response.text}")

    # get tiered pricing data
    pricing_url = "https://api-myaccount.hydroottawa.com/usage/rates"

    response = requests.post(pricing_url, headers=headers, json=request_body)

    if response.status_code == 200:
      pricing_data = response.json()
      tiered_pricing_data = pricing_data["tieredRates"]
    else:
      raise Exception(f"Failed to obtain pricing data: {response.status_code}\n{response.text}")

    return {
      "total_usage": total_usage,
      "tiered_pricing_data": tiered_pricing_data,
    }
