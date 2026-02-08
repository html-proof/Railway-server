from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any
from app.firebase_utils import get_db_ref
import time

router = APIRouter()

@router.get("/playlists/{uid}")
def get_playlists(uid: str):
    try:
        # New Schema: users/{uid}/library/playlists
        ref = get_db_ref(f"users/{uid}/library/playlists")
        playlists = ref.get()
        return playlists if playlists else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/playlists/{uid}")
def create_playlist(uid: str, name: str = Body(..., embed=True)):
    try:
        # New Schema: users/{uid}/library/playlists
        ref = get_db_ref(f"users/{uid}/library/playlists")
        new_playlist_ref = ref.push()
        new_playlist_ref.set({
            "name": name,
            "created_at": int(time.time()),
            "tracks": {}
        })
        return {"id": new_playlist_ref.key, "name": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/playlists/{uid}/{playlist_id}/add")
def add_to_playlist(uid: str, playlist_id: str, track: Dict[str, Any] = Body(...)):
    try:
        # New Schema: users/{uid}/library/playlists/{playlist_id}/tracks
        ref = get_db_ref(f"users/{uid}/library/playlists/{playlist_id}/tracks")
        ref.push(track)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/liked/{uid}")
def get_liked_songs(uid: str):
    try:
        ref = get_db_ref(f"users/{uid}/library/liked_songs")
        liked_songs = ref.get()
        if not liked_songs:
            return []
        # RTDB returns a dict of {push_id: song_data} or {song_id: song_data}
        # We'll normalize it to a list
        return list(liked_songs.values()) if isinstance(liked_songs, dict) else liked_songs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/liked/{uid}")
def toggle_like_song(uid: str, track: Dict[str, Any] = Body(...)):
    try:
        song_id = track.get("id")
        if not song_id:
            raise HTTPException(status_code=400, detail="Song ID is required")
            
        ref = get_db_ref(f"users/{uid}/library/liked_songs/{song_id}")
        existing = ref.get()
        
        if existing:
            ref.delete()
            return {"status": "unliked", "song_id": song_id}
        else:
            ref.set(track)
            return {"status": "liked", "song_id": song_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/playlists/{uid}/{playlist_id}")
def delete_playlist(uid: str, playlist_id: str):
    try:
        ref = get_db_ref(f"users/{uid}/library/playlists/{playlist_id}")
        ref.delete()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
