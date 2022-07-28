from pydantic import BaseModel, EmailStr
from pydantic.types import conint

from typing import Optional
from datetime import datetime

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

class PostVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class CreatePost(PostBase):
    pass

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None