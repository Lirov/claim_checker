import httpx
from typing import List, Dict, Any, Optional
import os

EVIDENCE_URL = os.getenv("EVIDENCE_URL", "http://evidence:8000")


class WikiClient:
    def __init__(self):
        self.base_url = EVIDENCE_URL
        self.session = httpx.AsyncClient(timeout=30.0)

    async def search_evidence(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for evidence using the evidence service
        """
        try:
            response = await self.session.get(
                f"{self.base_url}/wikipedia/search",
                params={"query": query, "limit": limit}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error searching evidence: {e}")
            return []

    async def get_summary(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Get Wikipedia page summary by title
        """
        try:
            response = await self.session.get(f"{self.base_url}/wikipedia/summary/{title}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting summary for {title}: {e}")
            return None

    async def close(self):
        await self.session.aclose()


# Global client instance
wiki_client = WikiClient()
