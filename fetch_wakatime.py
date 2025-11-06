import requests
import json
import os
import sys
import time
from datetime import date, timedelta

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Validate API key
api_key = os.environ.get("WAKATIME_API_KEY")
if not api_key or not api_key.startswith("waka_"):
    print("Error: Invalid or missing WAKATIME_API_KEY", file=sys.stderr)
    sys.exit(1)

today = date.today()
last_week = today - timedelta(days=7)

url = f"https://api.wakatime.com/api/v1/users/current/summaries?range={last_week},{today}"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

# Retry loop with exponential backoff
for attempt in range(MAX_RETRIES):
    try:
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()

            # Validate expected structure
            if not isinstance(data, dict):
                raise ValueError("Invalid response structure from WakaTime API: expected dict")

            # Check for expected fields
            if "data" not in data and "cumulative_total" not in data:
                raise ValueError("Invalid response structure: missing 'data' or 'cumulative_total' fields")

            with open("wakatime_data.json", "w") as f:
                json.dump(data, f, indent=2)

            print("✓ Successfully fetched WakaTime data")
            sys.exit(0)

        elif response.status_code == 429:
            print(f"Rate limited. Retrying in {RETRY_DELAY}s... (attempt {attempt + 1}/{MAX_RETRIES})", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
        elif response.status_code == 401:
            print("Error: Unauthorized. Check your WAKATIME_API_KEY", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"HTTP Error {response.status_code}: {response.text}", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)

    except requests.exceptions.Timeout:
        print(f"Timeout error (attempt {attempt + 1}/{MAX_RETRIES})", file=sys.stderr)
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error (attempt {attempt + 1}/{MAX_RETRIES}): {e}", file=sys.stderr)
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)

    except requests.exceptions.RequestException as e:
        print(f"Request error (attempt {attempt + 1}/{MAX_RETRIES}): {e}", file=sys.stderr)
        if attempt < MAX_RETRIES - 1:
            time.sleep(RETRY_DELAY)

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

print("✗ Failed to fetch WakaTime data after all retries", file=sys.stderr)
sys.exit(1)