from pydantic import BaseModel
from typing import Literal
from datetime import date

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    gender: Literal ["Male", "Female"]
    role: Literal ["customer", "admin", "superadmin"]
    weight: float
    height: float
    birthdate: date

class UserInDB(User):
    password: str