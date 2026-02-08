import yt_dlp
from typing import List, Dict

def get_artist_details(artist_id: str):
    # In a real scenario with just yt-dlp, "artist_id" might be a channel ID or query
    # For this implementation, we'll treat it as a query or channel URL if possible.
    # We will search for the artist channel.
    
    query = f"{artist_id} channel"
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'default_search': 'ytsearch1'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info and info['entries']:
                entry = info['entries'][0]
                return {
                    "id": entry.get("id"),
                    "name": entry.get("title"),
                    "thumbnail": entry.get("thumbnail"), # often null in flat extract
                    "channel_url": entry.get("url")
                }
    except Exception as e:
        print(f"Error fetching artist: {e}")
    return None

def get_artist_top_tracks(artist_name: str, limit: int = 10) -> List[Dict]:
    # Search for "Artist Name topic" or just "Artist Name" with strict song filtering
    query = f"{artist_name} top songs"
    
    # Re-use the existing search logic ideally, but we'll build a specific one here
    # to ensure we get "Top Tracks"
    
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'default_search': f'ytsearch{limit * 2}' # fetch more to filter
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
        tracks = []
        if 'entries' in info:
            for entry in info['entries']:
                # Basic filtering to ensure it looks like a song
                title = entry.get("title", "").lower()
                if "full album" in title or "playlist" in title:
                    continue
                    
                tracks.append({
                    "id": entry.get("id"),
                    "title": entry.get("title"),
                    "duration": entry.get("duration"),
                    "thumbnail": entry.get("thumbnail") # placeholder
                })
        return tracks[:limit]

    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        return []

def get_artist_albums(artist_name: str, limit: int = 5) -> List[Dict]:
    query = f"{artist_name} full album"
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'default_search': f'ytsearch{limit}'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
        
        albums = []
        if 'entries' in info:
            for entry in info['entries']:
                albums.append({
                     "id": entry.get("id"),
                     "title": entry.get("title"),
                     "thumbnail": entry.get("thumbnail")
                })
        return albums
            
    except Exception as e:
        print(f"Error fetching albums: {e}")
        return []
