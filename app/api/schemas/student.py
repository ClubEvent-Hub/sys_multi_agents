from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    field_of_study: Optional[str] = None
    year_level: Optional[int] = None


class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    field_of_study: Optional[str]
    year_level: Optional[int]
    created_at: datetime
    updated_at: datetime


class ProfileCreate(BaseModel):
    bio: Optional[str] = None
    goals: Optional[str] = None
    notification_preferences: Optional[str] = None


class ProfileUpdate(BaseModel):
    bio: Optional[str] = None
    goals: Optional[str] = None
    notification_preferences: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    student_id: int
    bio: Optional[str]
    goals: Optional[str]
    notification_preferences: Optional[str]
    last_updated: datetime


class DeleteResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime