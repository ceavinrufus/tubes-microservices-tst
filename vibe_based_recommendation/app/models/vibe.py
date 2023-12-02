from pydantic import BaseModel
from datetime import date
from typing import Literal
        
class Vibe(BaseModel):
    activity: Literal ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]
    mood: Literal ["happy", "loved", "focus", "chill", "sad", "scared", "angry", "neutral"] = None

class VibeRecommendation(Vibe):
    gender: Literal ["Male", "Female"]
    weather: bool

class VibeReq(Vibe):
    date: date

class VibeInDB(Vibe):
    username: str