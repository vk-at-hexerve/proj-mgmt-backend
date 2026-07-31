from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    pass

class UserCreate(UserBase):
    password: str
    system_role_id: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    system_role_id: Optional[str] = None

class UserResponse(UserBase):
    id: str
    role: Optional[str] = None
    system_role_id: Optional[str] = None
    created_at: Optional[datetime] = None
    internal_user: Optional[int] = None

    class Config:
        from_attributes = True

class ExternalUserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    system_role_id: Optional[str] = None

class ExternalUserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    system_role_id: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
