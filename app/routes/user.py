from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models.user import User, UserInDB, CreateUser
from app.models.token import Token
from app.middleware.auth import get_password_hash, create_access_token, get_current_active_user, authenticate_user
from app.config.database import users_collection
import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 0))

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: CreateUser):
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    

    user_dict = UserInDB(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
        full_name=user.full_name,
        disabled=False,
        role="guest"
    )
    users_collection.insert_one(dict(user_dict))
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user



