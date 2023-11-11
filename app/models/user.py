from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None
    role: str or None = None

class UserInDB(User):
    password: str

class CreateUser(BaseModel):
    username: str
    email: str or None = None
    password: str
    full_name: str or None = None