import requests
#grabs the forum search URL
FORUM_SEARCH_URL = "https://community.n8n.io/search.json"

#Grabs and loops through workflows realted to n8n

def fetch_forum_workflows(country="US", limit=25):
    """
    Fetch workflows from n8n community forum.
    Increased result count to ensure coverage toward 50+ unique total workflows.
    """

    query = "workflow"
    params = {"q": query}

    response = requests.get(FORUM_SEARCH_URL, params=params).json()
    topics = response.get("topics", [])
    topics = topics[:limit]

    results = []

    for topic in topics:
        title = topic.get("title", "Unknown")
        views = topic.get("views", 0)
        replies = topic.get("reply_count", 0)
        likes = topic.get("like_count", 0)

        results.append({
            "workflow": title,
            "source": "Forum",
            "country": country,
            "views": views,
            "likes": likes,
            "comments": replies,
            "snapshot_date": None,
            "like_to_view_ratio": likes / views if views else 0,
            "comment_to_view_ratio": replies / views if views else 0,
        })

    return results
