from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    body: str

class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    user: UserResponse

    class Config:
        orm_mode = True

class CreatePost(PostBase):
    pass

class Login(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None