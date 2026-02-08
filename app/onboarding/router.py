from fastapi import APIRouter, HTTPException, Body
from typing import List
from app.onboarding.models import Country, Language, Artist, Mode, UserOnboardingData
from app.onboarding.data import COUNTRIES, LANGUAGES, ARTISTS, MODES
from app.firebase_utils import get_db_ref

router = APIRouter()

@router.get("/countries", response_model=List[Country])
def get_countries():
    return COUNTRIES

@router.get("/languages/{country_code}", response_model=List[Language])
def get_languages(country_code: str):
    langs = LANGUAGES.get(country_code.upper())
    if not langs:
        # Default to English if user country not found (or return Global list if we had one)
        return [{"code": "en", "name": "English"}]
    return langs

@router.get("/artists", response_model=List[Artist])
def get_artists(country_code: str, language_code: str):
    # Filter artists based on country and language
    # In a real app, this might query a database or external API
    filtered_artists = [
        artist for artist in ARTISTS 
        if artist["country_code"] == country_code and artist["language_code"] == language_code
    ]
    # Fallback to similar language artists if strict match yields few results
    if len(filtered_artists) < 3:
         filtered_artists.extend([
            artist for artist in ARTISTS 
            if artist["language_code"] == language_code and artist not in filtered_artists
        ])
    return filtered_artists

@router.get("/modes", response_model=List[Mode])
def get_modes():
    return MODES

@router.post("/save/{uid}")
def save_onboarding_data(uid: str, data: UserOnboardingData):
    try:
        ref = get_db_ref(f"users/{uid}/onboarding")
        # Validate logic (e.g. min 3 artists) - enforcing here as well
        if len(data.artist_ids) < 3:
             raise HTTPException(status_code=400, detail="Please select at least 3 artists.")
        
        # Save as map for Firebase (as per expert recommendation)
        artists_map = {aid: True for aid in data.artist_ids}
        modes_map = {mid: True for mid in data.mode_ids}

        onboarding_payload = {
            "country": {"code": data.country_code, "name": next((c["name"] for c in COUNTRIES if c["code"] == data.country_code), "")},
            "language": {"code": data.language_code, "name": "Unknown"}, # Simplified for now
            "artists": artists_map,
            "modes": modes_map,
            "completed": True
        }
        ref.set(onboarding_payload)
        return {"status": "success", "message": "Onboarding data saved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{uid}")
def get_onboarding_status(uid: str):
    try:
        ref = get_db_ref(f"users/{uid}/onboarding")
        data = ref.get()
        if data and data.get("completed"):
            return {"completed": True}
        return {"completed": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
