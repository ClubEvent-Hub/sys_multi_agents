from pydantic import BaseModel
from typing import Optional


class SkillCreate(BaseModel):
    name: str
    category: Optional[str] = None


class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None


class SkillResponse(BaseModel):
    id: int
    name: str
    category: Optional[str]


class DeleteResponse(BaseModel):
    success: bool
    message: str
    timestamp: str