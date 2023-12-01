from typing import List

def individual_serial(mood) -> dict:
    return {
        # "id": str(mood.get("_id", "")),  
        "mood_id": int(mood.get("id", "")),  
        "mood": mood.get("mood", ""),  
        "date": mood.get("date", ""),
        "time": mood.get("time", ""),
    }

def list_serial(moods) -> list:
    return [individual_serial(mood) for mood in moods]