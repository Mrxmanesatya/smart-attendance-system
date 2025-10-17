"""
User model and schemas
Defines user data structures and validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from enum import Enum


class UserRole(str, Enum):
    """User roles in the system"""
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    TRAINEE = "trainee"


class OrganizationType(str, Enum):
    """Types of organizations"""
    CORPORATE = "corporate"
    COLLEGE = "college"
    GYM = "gym"
    TRAINING_INSTITUTE = "training_institute"
    OTHER = "other"


class UserBase(BaseModel):
    """Base user schema with common fields"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    organization_type: OrganizationType
    org_name: str = Field(..., min_length=2, max_length=200)
    role: UserRole = UserRole.TRAINEE


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response (excludes password)"""
    id: str = Field(alias="_id")
    created_at: datetime
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john@example.com",
                "role": "trainee",
                "organization_type": "college",
                "org_name": "MIT",
                "created_at": "2025-01-01T00:00:00"
            }
        }


class UserInDB(UserBase):
    """User model as stored in database"""
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored in JWT token"""
    email: Optional[str] = None
    role: Optional[str] = None
