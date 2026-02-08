from fastapi import APIRouter, HTTPException, Body
from app.player.services import get_stream_url, get_lyrics
from app.firebase_utils import get_db_ref
import time

router = APIRouter()

@router.get("/stream/{video_id}")
def stream_track(video_id: str):
    url = get_stream_url(video_id)
    if not url:
        raise HTTPException(status_code=404, detail="Stream not found")
    return {"stream_url": url}

@router.get("/download/{video_id}")
def download_track(video_id: str):
    # For a web app, "download" often means getting the same stream URL 
    # but the frontend triggers the download. 
    # Here we return the high-quality stream URL.
    url = get_stream_url(video_id)
    if not url:
        raise HTTPException(status_code=404, detail="Download link not found")
    return {"download_url": url}

@router.get("/lyrics/{video_id}")
def get_track_lyrics(video_id: str):
    return get_lyrics(video_id)

@router.post("/sync/{uid}")
def sync_playback(uid: str, state: dict = Body(...)):
    """
    Syncs current playback state to users/{uid}/playback/now_playing
    State should include: video_id, title, artist, progress, timestamp, device_id.
    """
    try:
        ref = get_db_ref(f"users/{uid}/playback/now_playing")
        state["updated_at"] = int(time.time())
        ref.set(state)
        return {"status": "synced"}
    except Exception as e:
        print(f"Sync error: {e}")
        # Don't fail the request just because sync failed, it's a background task usually
        return {"status": "error", "detail": str(e)}
