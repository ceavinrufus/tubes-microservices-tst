from pydantic import BaseModel
from typing import List
from datetime import date

class Order(BaseModel):
    id: int
    date: date
    ticketPrice: float
    total: int
    movieId: int
    seats: List[str]
    username: str
