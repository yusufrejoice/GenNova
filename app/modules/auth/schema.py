from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProfileBase(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str
    created_at: datetime

class UserProfile(ProfileBase):
    pass

class TokenResponse(BaseModel):
    access_token: str
    user: UserProfile
