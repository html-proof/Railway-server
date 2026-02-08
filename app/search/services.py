import yt_dlp
from app.search.filters import filter_and_rank_results
from app.firebase_utils import get_firestore_client
import hashlib
import time

CACHE_DURATION = 3600 * 24  # 24 Hours

def get_cache_key(query: str) -> str:
    return hashlib.md5(query.lower().encode()).hexdigest()

def search_music(query: str, limit: int = 10):
    # 1. Check Cache
    ctx = get_firestore_client()
    cache_key = get_cache_key(query)
    cache_ref = ctx.collection("search_cache").document(cache_key)
    
    try:
        doc = cache_ref.get()
        if doc.exists:
            data = doc.to_dict()
            if time.time() - data.get("timestamp", 0) < CACHE_DURATION:
                print(f"Cache Hit for: {query}")
                return data.get("results")[:limit]
    except Exception as e:
        print(f"Cache Read Error: {e}")

    # 2. Fetch from yt-dlp (Cache Miss)
    fetch_limit = 30 
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'default_search': f'ytsearch{fetch_limit}'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            
        raw_results = []
        if 'entries' in info:
            for entry in info['entries']:
                if entry:
                    raw_results.append({
                        "id": entry.get("id"),
                        "title": entry.get("title"),
                        "duration": entry.get("duration", 0),
                        "uploader": entry.get("uploader"),
                        "url": entry.get("url"),
                        "thumbnail": entry.get("thumbnail") # Note: yt-dlp flat extract might not have high-res thumbnails
                    })
        
        # Apply Strict Filtering
        clean_results = filter_and_rank_results(raw_results, query)
        
        # 3. Save to Cache
        if clean_results:
            try:
                cache_ref.set({
                    "query": query,
                    "results": clean_results,
                    "timestamp": int(time.time())
                })
            except Exception as e:
                print(f"Cache Write Error: {e}")
        
        # Return only the top N requested
        return clean_results[:limit]

    except Exception as e:
        print(f"Search Error: {e}")
        return []
