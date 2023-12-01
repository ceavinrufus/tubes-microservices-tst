from pydantic import BaseModel
from datetime import date, time

class Mood(BaseModel):
    id: int
    mood: str
    date: date
    time: time