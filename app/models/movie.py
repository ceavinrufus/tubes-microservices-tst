from pydantic import BaseModel
from typing import List
from datetime import date

class Movie(BaseModel):
    id: int
    title: str
    genre: str
    original_language: str
    overview: str
    release_date: date
