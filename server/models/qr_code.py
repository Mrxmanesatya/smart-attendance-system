"""
QR Code model and schemas
Defines QR code data structures
"""
from datetime import datetime
from pydantic import BaseModel, Field


class QRCodeBase(BaseModel):
    """Base QR code schema"""
    session_id: str
    code_value: str
    expires_at: datetime


class QRCodeResponse(QRCodeBase):
    """Schema for QR code response"""
    id: str = Field(alias="_id")
    created_at: datetime
    is_expired: bool = False
    
    class Config:
        populate_by_name = True


class QRCodeInDB(QRCodeBase):
    """QR code model as stored in database"""
    created_at: datetime = Field(default_factory=datetime.utcnow)


class QRCodeDisplay(BaseModel):
    """Schema for displaying QR code to user"""
    qr_image_base64: str
    code_value: str
    expires_at: datetime
    session_id: str
    session_title: str
