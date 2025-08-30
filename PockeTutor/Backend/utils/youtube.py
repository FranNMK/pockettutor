# backend/utils/youtube.py
import os, requests

YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

def search_youtube(query: str, max_results: int = 5):
    if not YOUTUBE_KEY:
        return []
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_KEY
    }
    r = requests.get(url, params=params, timeout=10)
    items = r.json().get("items", [])
    results = []
    for it in items:
        vid = it["id"]["videoId"]
        results.append({
            "id": vid,
            "title": it["snippet"]["title"],
            "url": f"https://www.youtube.com/watch?v={vid}",
            "embed": f"https://www.youtube.com/embed/{vid}"
        })
    return results
