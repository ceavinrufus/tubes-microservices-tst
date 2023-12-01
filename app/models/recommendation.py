from pydantic import BaseModel
from typing import Literal
        
class RecCriteria(BaseModel):
    gender: Literal ["Male", "Female"]
    activity: Literal ["sedentary", "lightly_active", "moderately_active", "very_active", "extra_active"]
    mood: Literal ["happy", "loved", "focus", "chill", "sad", "scared", "angry", "neutral"] = None
    weather: bool

