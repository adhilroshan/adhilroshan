import google.generativeai as genai
import json
import os
import sys

# Validate API key
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key or not api_key.startswith("AIza"):
    print("Error: Invalid or missing GOOGLE_API_KEY", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

try:
    with open("wakatime_data.json", "r") as f:
        wakatime_data = json.load(f)
except FileNotFoundError:
    print("Error: wakatime_data.json not found", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in wakatime_data.json: {e}", file=sys.stderr)
    sys.exit(1)

def sanitize_for_prompt(data):
    """
    Sanitize WakaTime data to prevent prompt injection attacks.
    Extracts only safe, expected fields and validates structure.
    """
    try:
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")

        # Extract safe data from cumulative_total or first day's grand_total
        total_seconds = 0
        if "cumulative_total" in data:
            total_seconds = data["cumulative_total"].get("seconds", 0)
        elif "data" in data and len(data["data"]) > 0:
            total_seconds = data["data"][0].get("grand_total", {}).get("total_seconds", 0)

        # Extract languages (limit to top 10)
        languages = []
        if "data" in data and len(data["data"]) > 0:
            for day in data["data"]:
                for lang in day.get("languages", [])[:10]:
                    if "name" in lang and isinstance(lang["name"], str):
                        languages.append(lang["name"])

        # Extract projects (limit to top 10)
        projects = []
        if "data" in data and len(data["data"]) > 0:
            for day in data["data"]:
                for proj in day.get("projects", [])[:10]:
                    if "name" in proj and isinstance(proj["name"], str):
                        projects.append(proj["name"])

        # Deduplicate while preserving order
        languages = list(dict.fromkeys(languages))[:10]
        projects = list(dict.fromkeys(projects))[:10]

        safe_data = {
            "total_seconds": total_seconds,
            "languages": languages,
            "projects": projects
        }

        return json.dumps(safe_data, indent=2)

    except Exception as e:
        print(f"Error sanitizing data: {e}", file=sys.stderr)
        sys.exit(1)

def generate_natural_language_summary(data):
    """Generate AI summary with sanitized input to prevent prompt injection"""
    safe_data = sanitize_for_prompt(data)

    prompt = f"""Here is my coding activity summary from the last 7 days:
{safe_data}

Please provide a 2-3 sentence natural language summary focusing on:
- Total coding time (convert seconds to hours)
- Top 3 programming languages used
- Main projects worked on

Keep the tone friendly and concise."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI summary: {e}", file=sys.stderr)
        sys.exit(1)

summary = generate_natural_language_summary(wakatime_data)

# Validate summary is not empty
if not summary or not summary.strip():
    print("Error: Generated summary is empty", file=sys.stderr)
    sys.exit(1)

with open("wakatime_summary.txt", "w") as f:
    f.write(summary.strip())

print("✓ Successfully generated WakaTime summary")