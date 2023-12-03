from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.token import TokenData
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
from app.models.user import UserInDB
from app.config.database import users_collection
import os

load_dotenv(find_dotenv())
KEY = os.getenv("KEY")
ALGORITHM = os.getenv("ALGORITHM") 

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"])
    
    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def get_user(self, username: str):
        user_data = users_collection.find_one({"username": username})

        if not user_data is None:
            return UserInDB(**user_data)
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        
        return user
    
    def create_access_token(self, data: dict, expires_delta: timedelta or None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
        
    def get_current_user(self, token: str):
        credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        try:
            payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credential_exception
            
            token_data = TokenData(username=username)    
        except JWTError:
            raise credential_exception
        
        user = self.get_user(username=token_data.username)
        if user is None:
            raise credential_exception
        
        return dict(user)
