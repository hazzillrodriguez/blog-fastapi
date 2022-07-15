from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    body: str

class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Login(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None