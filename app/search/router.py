from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.search.services import search_music
from app.firebase_utils import get_db_ref
import time

router = APIRouter()

class SearchResult(BaseModel):
    id: str
    title: str
    duration: int
    uploader: Optional[str] = None
    thumbnail: Optional[str] = None
    score: Optional[int] = 0

@router.get("/quick", response_model=List[SearchResult])
def quick_search(query: str, uid: Optional[str] = None):
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    results = search_music(query, limit=10)
    
    # Save Search History if UID provided
    if uid:
        try:
            # New Schema: users/{uid}/history/search
            history_ref = get_db_ref(f"users/{uid}/history/search")
            history_ref.push({
                "query": query,
                "timestamp": int(time.time()),
                "top_result": results[0]["title"] if results else None
            })
        except Exception as e:
            print(f"Failed to save history: {e}")
            
    return results

@router.get("/exact")
def exact_search(query: str):
    # Returns the single best match
    results = search_music(query, limit=1)
    if not results:
        raise HTTPException(status_code=404, detail="No matching song found.")
    return results[0]
