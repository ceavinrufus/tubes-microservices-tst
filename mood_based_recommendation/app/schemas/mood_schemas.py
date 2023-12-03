def individual_serial(mood) -> dict:
    return {
        "username": mood.get("username", ""),
        "datetime": mood.get("datetime", ""),
        "notes": mood.get("notes", ""),
        "mood": mood.get("mood", ""),  
    }

def list_serial(moods) -> list:
    return [individual_serial(mood) for mood in moods]