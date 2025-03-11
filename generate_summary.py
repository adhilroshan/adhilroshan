import google.generativeai as genai
import json
import os

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

with open("wakatime_data.json", "r") as f:
    wakatime_data = json.load(f)

def generate_natural_language_summary(data):
    prompt = f"""
    Here is my coding activity from the last 7 days in json format: {data}.
    Please provide a concise and engaging natural language summary of my coding activity.
    Focus on the projects I worked on, the languages I used, and any interesting patterns.
    """
    response = model.generate_content(prompt)
    return response.text

summary = generate_natural_language_summary(wakatime_data)

with open("wakatime_summary.txt", "w") as f:
    f.write(summary)