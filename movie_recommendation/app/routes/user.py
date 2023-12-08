from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from datetime import timedelta
from app.middleware.authorization import JWTBearer
from app.models.user import User, UserInDB, UserLogin
from app.models.token import Token
from app.middleware.authentication import AuthHandler
from app.config.database import users_collection
import os

ACCESS_TOKEN_EXPIRE_MINUTES = 43200
SUPERADMIN_SECRET_KEY = os.getenv("SUPERADMIN_SECRET_KEY", 0)

router = APIRouter(tags=["Users"])
auth = AuthHandler()

@router.post("/register", response_model=Token)
async def register(user: UserInDB, superadmin_key: Optional[str] = Query(None, alias="key")):
    if superadmin_key != SUPERADMIN_SECRET_KEY and user.role in ["superadmin", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="Invalid or insufficient permissions"
        )
    
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    
    user_dict = UserInDB(
        username=user.username,
        email=user.email,
        password=auth.get_password_hash(user.password),
        full_name=user.full_name,
        gender=user.gender,
        role=user.role,
        weight=float(user.weight),
        height=float(user.height),
        birthdate=user.birthdate
    )
    user_dict.birthdate=user_dict.birthdate.isoformat()
    users_collection.insert_one(dict(user_dict))

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(form_data: UserLogin):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(JWTBearer())):
    return current_user
