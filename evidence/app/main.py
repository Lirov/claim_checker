from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from .wikipedia import wiki_client

app = FastAPI(
    title="Claim-Checker Evidence Service",
    description="Service for fetching evidence from Wikipedia and other sources",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Claim-Checker Evidence Service"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "evidence"}


@app.get("/wikipedia/search")
async def search_wikipedia(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search Wikipedia for evidence related to a query
    """
    if not query or len(query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    
    try:
        results = await wiki_client.search_pages(query, limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching Wikipedia: {str(e)}")


@app.get("/wikipedia/summary/{title:path}")
async def get_wikipedia_summary(title: str) -> Dict[str, Any]:
    """
    Get Wikipedia page summary by title
    """
    try:
        summary = await wiki_client.get_page_summary(title)
        if summary:
            return {
                "title": title,
                "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                "snippet": summary
            }
        else:
            raise HTTPException(status_code=404, detail="Page not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting summary: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    await wiki_client.close()
