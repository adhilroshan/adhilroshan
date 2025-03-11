import requests
import json
import os
from datetime import date, timedelta

api_key = os.environ.get("WAKATIME_API_KEY")
today = date.today()
last_week = today - timedelta(days=7)

url = f"https://api.wakatime.com/api/v1/users/current/summaries?range={last_week},{today}"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open("wakatime_data.json", "w") as f:
        json.dump(response.json(), f)
else:
    print(f"Error fetching WakaTime data: {response.status_code}")