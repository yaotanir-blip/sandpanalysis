import json
import requests
from sandpa import config

key = config.get_api_key()
url =  f"{config.API_BASE_URL}/SPY/prices"    # config.API_BASE_URL + the SPY prices path
params = {"startDate":"2024-01-02","endDate":"2024-01-08"}    # one week is enough, e.g. 2024-01-02 to 2024-01-08
headers = {"Authorization":f"Token {key}"}   # check Tiingo's docs: how should the token be sent?

response = requests.get(url, params=params, headers=headers, timeout=10)
print(response.status_code)
print(response.url)
data = response.json()
print(len(data))
print(data[0])
# print: the status code, how many rows came back, and the first row
# save the JSON to tests/fixtures/sample_response.json with json.dump(..., indent=2)
with open("tests/fixtures/sample_response.json", "w") as f:   
    json.dump(data, f, indent=2)                            