from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.artist.services import get_artist_details, get_artist_top_tracks, get_artist_albums

router = APIRouter()

@router.get("/{artist_query}")
def get_artist_profile(artist_query: str):
    # We use the query/name to find details. 
    # In a real app, this would be an ID from a database.
    details = get_artist_details(artist_query)
    if not details:
        # Fallback if channel search fails, just return the name
        return {"name": artist_query, "id": artist_query}
    return details

@router.get("/{artist_name}/top-tracks")
def get_top_tracks(artist_name: str):
    return get_artist_top_tracks(artist_name)

@router.get("/{artist_name}/albums")
def get_albums(artist_name: str):
    return get_artist_albums(artist_name)
