from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ClubUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    description: Optional[str] = None
    mission: Optional[str] = None
    history: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    personality_style: Optional[str] = None


class ClubResponse(BaseModel):
    id: int
    name: str
    email: str
    description: Optional[str]
    mission: Optional[str]
    history: Optional[str]
    contact_email: Optional[str]
    website: Optional[str]
    logo_url: Optional[str]
    personality_style: Optional[str]
    created_at: datetime
    updated_at: datetime


class DeleteResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime