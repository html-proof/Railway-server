from fastapi import APIRouter, Body
from app.recommendation.scoring import get_recommendation_candidates
from app.recommendation.strategies import generate_smart_queue
from typing import Dict, List

router = APIRouter()

@router.post("/home")
def get_home_recommendations(user_profile: Dict = Body(...)):
    # Mock current track as None for home page
    recs = get_recommendation_candidates(user_profile, None)
    return {"sections": [{"title": "Made for You", "items": recs}]}

@router.post("/next")
def get_next_tracks(current_track: Dict = Body(...), history: List[Dict] = Body([])):
    queue = generate_smart_queue(current_track, history)
    return {"queue": queue}
