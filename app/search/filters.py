import re

# Strict Blockset
BLOCK_KEYWORDS = [
    "trailer", "teaser", "reaction", "interview", "dialogue",
    "scene", "bgm", "remix", "cover", "shorts", "status",
    "full movie", "movie review", "podcast", "speech", "news",
    "live", "dj", "mashup", "karaoke", "instrumental", "behind the scenes",
    "vlog", "gameplay", "tutorial", "review", "react", "opinion"
]

# High Quality Boosters
BOOST_KEYWORDS = [
    "official audio", "official video", "lyrical", "song", 
    "full song", "audio", "video song", "soundtrack", "hq", "hd"
]

# Trusted Music Channels (Partial List - Expand as needed)
TRUSTED_CHANNELS = [
    "t-series", "sony music", "zeemusic", "vevo", "speed records",
    "tips official", "saregama", "ynt records", "aditya music",
    "eros now", "think music", "lahari music", "geetha arts",
    "sony music south", "sony music india", "universal music",
    "warner music", "spinnin' records", "monstercat"
]

def clean_title(title: str) -> str:
    return re.sub(r'\(.*?\)|\[.*?\]', '', title).strip().lower()

def is_valid_duration(duration: int) -> bool:
    # Songs are typically 2 to 10 minutes
    return 120 <= duration <= 600

def score_result(result: dict, query: str) -> int:
    title = result.get("title", "").lower()
    duration = result.get("duration", 0)
    uploader = result.get("uploader", "").lower()
    score = 0

    # 1. Critical Blocking
    if any(word in title for word in BLOCK_KEYWORDS):
        return -100

    if not is_valid_duration(duration):
        return -50

    # 2. Channel Trust (Huge Boost)
    if any(channel in uploader for channel in TRUSTED_CHANNELS) or "topic" in uploader:
        score += 20
    
    # 3. Content Type Boosting
    if any(word in title for word in BOOST_KEYWORDS):
        score += 10
    
    # 4. Exact Match
    if query.lower() in title:
        score += 5
        
    return score

def filter_and_rank_results(results: list, query: str) -> list:
    ranked_results = []
    seen_titles = set()

    for res in results:
        score = score_result(res, query)
        
        # Only accept positive scores or effectively neutral ones that passed filters
        if score >= 0: 
            clean = clean_title(res.get("title", ""))
            
            # Deduplication
            if clean in seen_titles:
                continue
            seen_titles.add(clean)
            
            res["score"] = score
            ranked_results.append(res)
    
    # Sort by score descending
    ranked_results.sort(key=lambda x: x["score"], reverse=True)
    
    return ranked_results[:10]
