from pydantic import BaseModel
from datetime import date, time
from typing import Literal

class Vibe(BaseModel):
    date: date
    activity: Literal ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]
    mood: Literal ["happy", "loved", "focus", "chill", "sad", "scared", "angry", "neutral"] = None

class VibeInDB(Vibe):
    username: str