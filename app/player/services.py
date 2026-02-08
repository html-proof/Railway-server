import yt_dlp

def get_stream_url(video_id: str) -> str:
    try:
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio[ext=m4a]/best',
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_id, download=False)
            return info.get("url")
    except Exception as e:
        print(f"Error getting stream URL: {e}")
        return None

def get_lyrics(video_id: str) -> dict:
    # Placeholder for Lyrics
    # In a real implementation, we could use a library like `syncedlyrics` or scrape Genius/Musixmatch
    # For now, we return a mock or try to get subtitles if available from yt-dlp
    
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'writesubtitles': True,
            'allsubtitles': True,
        }
        # This is a bit heavy just for checking subs, and yt-dlp handling of subs in memory is tricky without download.
        # We'll stick to a placeholder for the "Premier" feature request.
        return {"lyrics": "Lyrics not available for this track.", "sync": False}
    except Exception:
        return {"lyrics": "Error fetching lyrics.", "sync": False}
