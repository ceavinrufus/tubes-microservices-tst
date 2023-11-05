from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Wishlist(BaseModel):
    id: str
    date: date
    startAt: str
    seats: List[dict]
    ticketPrice: float
    total: float
    movieId: str
    cinemaId: str
    username: str
    phone: str
    checkin: bool
