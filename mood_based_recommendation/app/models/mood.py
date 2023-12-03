from pydantic import BaseModel
from datetime import datetime
from typing import Literal
        
class Mood(BaseModel):
    mood: Literal ["happy", "loved", "focus", "chill", "sad", "scared", "angry", "neutral"] = None

class MoodReq(Mood):
    notes: str
    datetime: datetime

class MoodInDB(MoodReq):
    username: str