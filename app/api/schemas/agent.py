
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AgentRequest(BaseModel):
    message: str = Field(..., description="User's message or query")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Optional context")


class AgentResponse(BaseModel):
    response: str = Field(..., description="Agent's response")
    agent: str = Field(..., description="Which agent responded")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatbotRequest(BaseModel):
    club_id: int = Field(..., description="Club ID")
    message: str = Field(..., description="User's message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "club_id": 1,
                "message": "What is this club about?"
            }
        }


class RecommendationRequest(BaseModel):
    student_id: int = Field(..., description="Student ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": 1
            }
        }


class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "AI workshop",
                "filters": {"event_type": "workshop"}
            }
        }