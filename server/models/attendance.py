"""
Attendance model and schemas
Defines attendance record structures
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class AttendanceStatus(str, Enum):
    """Attendance status options"""
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"


class AttendanceMethod(str, Enum):
    """Method used to mark attendance"""
    QR_CODE = "qr_code"
    MANUAL = "manual"
    ADMIN_OVERRIDE = "admin_override"


class AttendanceBase(BaseModel):
    """Base attendance schema"""
    session_id: str
    user_id: str
    status: AttendanceStatus = AttendanceStatus.PRESENT
    method: AttendanceMethod = AttendanceMethod.QR_CODE


class AttendanceCreate(BaseModel):
    """Schema for marking attendance via QR scan"""
    qr_code_value: str


class AttendanceResponse(AttendanceBase):
    """Schema for attendance response"""
    id: str = Field(alias="_id")
    timestamp: datetime
    
    class Config:
        populate_by_name = True


class AttendanceInDB(AttendanceBase):
    """Attendance model as stored in database"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AttendanceStats(BaseModel):
    """Schema for attendance statistics"""
    total_sessions: int
    attended: int
    missed: int
    late: int
    attendance_percentage: float
