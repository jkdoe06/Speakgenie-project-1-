import os
import requests
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / '.env'
load_dotenv(env_path)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
print("Loaded KEY:", YOUTUBE_API_KEY)

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

params = {
    "part": "snippet",
    "q": "n8n workflow",
    "type": "video",
    "regionCode": "US",
    "maxResults": 5,
    "key": YOUTUBE_API_KEY
}

r = requests.get(SEARCH_URL, params=params)
print("Status:", r.status_code)
print("Response:", r.json())
