import httpx
import re
from typing import List, Optional, Dict, Any
import os

WIKIPEDIA_API_URL = os.getenv("WIKIPEDIA_API_URL", "https://en.wikipedia.org/api/rest_v1")


class WikipediaClient:
    def __init__(self):
        self.base_url = WIKIPEDIA_API_URL
        self.session = httpx.AsyncClient(timeout=10.0)

    async def search_pages(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search Wikipedia pages for a given query
        """
        try:
            # Use Wikipedia's search API
            search_url = f"https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": limit,
                "srnamespace": 0,  # Main namespace only
                "srprop": "snippet|title"
            }
            
            response = await self.session.get(search_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get("query", {}).get("search", []):
                # Get page summary for each search result
                summary = await self.get_page_summary(item["title"])
                if summary:
                    results.append({
                        "title": item["title"],
                        "url": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}",
                        "snippet": summary,
                        "score": 0.0  # Will be calculated by verifier
                    })
            
            return results
            
        except Exception as e:
            print(f"Error searching Wikipedia: {e}")
            return []

    async def get_page_summary(self, title: str) -> Optional[str]:
        """
        Get page summary from Wikipedia REST API
        """
        try:
            # Clean title for URL
            clean_title = title.replace(" ", "_")
            url = f"{self.base_url}/page/summary/{clean_title}"
            
            response = await self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            return data.get("extract", "")
            
        except Exception as e:
            print(f"Error getting page summary for {title}: {e}")
            return None

    async def close(self):
        await self.session.aclose()


# Global client instance
wiki_client = WikipediaClient()
