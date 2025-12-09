import os
import requests
from pathlib import Path
from dotenv import load_dotenv

#Paths to the env to grab the correct api key 
#Fetchs trending workflows related to n8n and loops through

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

TRENDS_API_KEY = os.getenv("TRENDS_API_KEY")
SEARCH_URL = "https://serpapi.com/search.json"


def fetch_trending_workflows(country="US"):
    """
    Fetch trending search terms around 'n8n' from Google Trends.
    Adds extra workflows to reach assignment volume.
    """

    params = {
        "engine": "google_trends",
        "hl": "en-US",
        "geo": country.upper(),
        "q": "n8n workflow",
        "api_key": TRENDS_API_KEY,
    }

    r = requests.get(SEARCH_URL, params=params).json()
    items = r.get("interest_over_time", {}).get("timeline_data", [])
    if not items:
        return []

    results = []
    for item in items[:20]:  # collect more to help reach 50 unique workflows
        keyword = item["values"][0]["keyword"]

        results.append({
            "workflow": keyword,
            "source": "Trends",
            "country": country.upper(),
            "views": 0,
            "likes": 0,
            "comments": 0,
            "snapshot_date": None,
            "like_to_view_ratio": 0,
            "comment_to_view_ratio": 0,
        })

    return results
