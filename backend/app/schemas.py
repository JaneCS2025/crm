from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    tel: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    # Use 'str' here because SQLite returns timestamps as strings
    created_at: str 
    updated_at: str

    class Config:
        from_attributes = True  # This allows Pydantic to read 'sqlite3.Row'

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    tel: Optional[str] = None
    password: Optional[str] = None # Now optional!