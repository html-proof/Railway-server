import random

def get_recommendation_candidates(user_profile, current_track, limit=20):
    # In a real system, this would query a vector DB or advanced matching engine.
    # Here we mock the behavior of the 60/25/15 split requested by the user.
    
    recs = []
    
    # 1. Similar to User Taste / Current Track (60%)
    # Logic: Search for similar genre/mood/language
    target_sim = int(limit * 0.6)
    recs.extend(_fetch_sim_tracks(current_track, target_sim))
    
    # 2. Discovery (25%)
    # Logic: Same language but different artists
    target_disc = int(limit * 0.25)
    recs.extend(_fetch_discovery_tracks(user_profile, target_disc))
    
    # 3. Trending (15%)
    # Logic: Top charts for user's country
    target_trend = limit - len(recs)
    recs.extend(_fetch_trending_tracks(user_profile, target_trend))
    
    return recs

def _fetch_sim_tracks(track, count):
    # Mock return
    return [{"id": f"sim_{i}", "title": f"Similar Song {i}", "type": "similar"} for i in range(count)]

def _fetch_discovery_tracks(profile, count):
    return [{"id": f"disc_{i}", "title": f"New Discovery {i}", "type": "discovery"} for i in range(count)]

def _fetch_trending_tracks(profile, count):
    return [{"id": f"trend_{i}", "title": f"Trending Hit {i}", "type": "trending"} for i in range(count)]
