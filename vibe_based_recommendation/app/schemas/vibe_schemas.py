from typing import List

def individual_serial(vibe) -> dict:
    return {
        "date": vibe.get("date", ""),
        "mood": vibe.get("mood", ""),  
        "activity": vibe.get("activity", ""),  
    }

def list_serial(vibes) -> list:
    return [individual_serial(vibe) for vibe in vibes]