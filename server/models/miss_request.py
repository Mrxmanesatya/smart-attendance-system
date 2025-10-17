"""
Miss Request model and schemas
Defines missed attendance request structures
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class RequestStatus(str, Enum):
    """Status of miss request"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class MissRequestBase(BaseModel):
    """Base miss request schema"""
    session_id: str
    reason: str = Field(..., min_length=10, max_length=500)


class MissRequestCreate(MissRequestBase):
    """Schema for creating a miss request"""
    pass


class MissRequestUpdate(BaseModel):
    """Schema for updating miss request (admin action)"""
    status: RequestStatus
    admin_response: Optional[str] = Field(None, max_length=500)


class MissRequestResponse(MissRequestBase):
    """Schema for miss request response"""
    id: str = Field(alias="_id")
    user_id: str
    status: RequestStatus
    admin_response: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True


class MissRequestInDB(MissRequestBase):
    """Miss request model as stored in database"""
    user_id: str
    status: RequestStatus = RequestStatus.PENDING
    admin_response: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
