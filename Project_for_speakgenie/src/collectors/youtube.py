import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the project root (two levels above)
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)
#Grabs the youtube key from .env 
#Access the search and detail URL for youtube v3
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
DETAILS_URL = "https://www.googleapis.com/youtube/v3/videos"

#Grabs metrics and data from youtubes API and creates a workflow
#Grabs and loops through videos realted to n8n
def fetch_youtube_workflows(country="US", max_pages=3, page_size=15):
    

    query = "n8n workflow"
    results = []
    next_page = None

    for _ in range(max_pages):
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "regionCode": country,
            "maxResults": page_size,
            "key": YOUTUBE_API_KEY
        }
        if next_page:
            params["pageToken"] = next_page

        search_response = requests.get(SEARCH_URL, params=params).json()
        items = search_response.get("items", [])
        if not items:
            break

        # Pagination token
        next_page = search_response.get("nextPageToken")

        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]

            # Fetch statistics separately (views, likes, comments)
            stats_params = {
                "part": "statistics",
                "id": video_id,
                "key": YOUTUBE_API_KEY
            }
            stats_response = requests.get(DETAILS_URL, params=stats_params).json()
            stats = stats_response["items"][0]["statistics"]

            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))

            results.append({
                "workflow": title,
                "source": "YouTube",
                "country": country,
                "views": views,
                "likes": likes,
                "comments": comments,
                "snapshot_date": None,
                "like_to_view_ratio": likes / views if views else 0,
                "comment_to_view_ratio": comments / views if views else 0,
            })

        if not next_page:
            break

    return results
