from pydantic import BaseModel, EmailStr
from datetime import datetime

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