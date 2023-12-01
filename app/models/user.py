from pydantic import BaseModel
from typing import Literal
from datetime import date

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    gender: Literal ["Male", "Female"]
    disabled: bool or None = None
    role: str or None = None
    weight: float
    height: float
    birthdate: date

class UserInDB(User):
    password: str

class CreateUser(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    gender: Literal ["Male", "Female"]
    birthdate: date
    password: str
    weight: float
    height: float