"""
Session model and schemas
Defines session/class data structures
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SessionBase(BaseModel):
    """Base session schema"""
    title: str = Field(..., min_length=3, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    start_time: datetime
    end_time: datetime


class SessionCreate(SessionBase):
    """Schema for creating a new session"""
    pass


class SessionResponse(SessionBase):
    """Schema for session response"""
    id: str = Field(alias="_id")
    created_by: str
    qr_code_id: Optional[str] = None
    active: bool = True
    created_at: datetime
    
    class Config:
        populate_by_name = True


class SessionInDB(SessionBase):
    """Session model as stored in database"""
    created_by: str  # User ID who created the session
    qr_code_id: Optional[str] = None
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
