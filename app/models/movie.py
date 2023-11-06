from pydantic import BaseModel
from typing import List
from datetime import date

class Genre(BaseModel):
    id: int
    name: str

class Movie(BaseModel):
    id: int
    title: str
    genres: List[Genre]
    original_language: str
    overview: str
    release_date: date
