"""
Attendance management routes
Handles QR code scanning, attendance marking, and history retrieval
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from database import get_database
from models.attendance import (
    AttendanceCreate, 
    AttendanceResponse, 
    AttendanceInDB, 
    AttendanceStats,
    AttendanceStatus,
    AttendanceMethod
)
from models.user import TokenData, UserRole
from utils.auth import get_current_user
from utils.qr_generator import is_qr_expired

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.post("/scan", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance_qr(
    attendance: AttendanceCreate,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Mark attendance by scanning QR code
    
    Available to all authenticated users (primarily Trainees).
    
    - **qr_code_value**: The QR code value scanned by the user
    
    Process:
    1. Validates QR code exists and hasn't expired
    2. Retrieves associated session
    3. Marks attendance for the user
    4. Prevents duplicate attendance marking
    """
    # Find QR code in database
    qr_code = await db.qr_codes.find_one({"code_value": attendance.qr_code_value})
    
    if not qr_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid QR code"
        )
    
    # Check if QR code has expired
    if is_qr_expired(qr_code["expires_at"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="QR code has expired"
        )
    
    # Get session
    session_id = qr_code["session_id"]
    try:
        session = await db.sessions.find_one({"_id": ObjectId(session_id)})
    except:
        session = await db.sessions.find_one({"_id": session_id})
    
    if not session or not session.get("active", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or inactive"
        )
    
    # Get user ID
    user = await db.users.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_id = str(user["_id"])
    
    # Check if attendance already marked for this session
    existing_attendance = await db.attendance_records.find_one({
        "session_id": session_id,
        "user_id": user_id
    })
    
    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already marked for this session"
        )
    
    # Determine attendance status based on timing
    current_time = datetime.utcnow()
    session_start = session["start_time"]
    
    # Mark as late if current time is after session start
    if current_time > session_start:
        attendance_status = AttendanceStatus.LATE
    else:
        attendance_status = AttendanceStatus.PRESENT
    
    # Create attendance record
    attendance_in_db = AttendanceInDB(
        session_id=session_id,
        user_id=user_id,
        status=attendance_status,
        method=AttendanceMethod.QR_CODE
    )
    
    # Insert into database
    result = await db.attendance_records.insert_one(attendance_in_db.model_dump())
    
    # Retrieve created attendance record
    created_attendance = await db.attendance_records.find_one({"_id": result.inserted_id})
    created_attendance["_id"] = str(created_attendance["_id"])
    
    return AttendanceResponse(**created_attendance)


@router.get("/user/{user_id}", response_model=List[AttendanceResponse])
async def get_user_attendance(
    user_id: str,
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Get attendance history for a specific user
    
    - **user_id**: ID of the user
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    
    Users can view their own attendance.
    Admins and Instructors can view anyone's attendance.
    """
    # Get current user's ID
    current_user_doc = await db.users.find_one({"email": current_user.email})
    current_user_id = str(current_user_doc["_id"])
    
    # Permission check: users can only view their own attendance unless they're admin/instructor
    if (current_user.role not in [UserRole.ADMIN.value, UserRole.INSTRUCTOR.value] 
        and user_id != current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this user's attendance"
        )
    
    # Fetch attendance records
    cursor = db.attendance_records.find(
        {"user_id": user_id}
    ).sort("timestamp", -1).skip(skip).limit(limit)
    
    attendance_records = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for record in attendance_records:
        record["_id"] = str(record["_id"])
    
    return [AttendanceResponse(**record) for record in attendance_records]


@router.get("/user/{user_id}/stats", response_model=AttendanceStats)
async def get_user_attendance_stats(
    user_id: str,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Get attendance statistics for a user
    
    Returns total sessions, attended, missed, late, and attendance percentage.
    """
    # Get current user's ID
    current_user_doc = await db.users.find_one({"email": current_user.email})
    current_user_id = str(current_user_doc["_id"])
    
    # Permission check
    if (current_user.role not in [UserRole.ADMIN.value, UserRole.INSTRUCTOR.value] 
        and user_id != current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this user's statistics"
        )
    
    # Get all active sessions
    total_sessions = await db.sessions.count_documents({"active": True})
    
    # Get attendance records for user
    attendance_records = await db.attendance_records.find({"user_id": user_id}).to_list(length=None)
    
    # Count by status
    attended = sum(1 for r in attendance_records if r["status"] == AttendanceStatus.PRESENT.value)
    late = sum(1 for r in attendance_records if r["status"] == AttendanceStatus.LATE.value)
    total_attended = attended + late
    missed = total_sessions - total_attended
    
    # Calculate percentage
    attendance_percentage = (total_attended / total_sessions * 100) if total_sessions > 0 else 0
    
    return AttendanceStats(
        total_sessions=total_sessions,
        attended=attended,
        missed=missed,
        late=late,
        attendance_percentage=round(attendance_percentage, 2)
    )


@router.get("/session/{session_id}", response_model=List[dict])
async def get_session_attendance(
    session_id: str,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN, UserRole.INSTRUCTOR])),
    db=Depends(get_database)
):
    """
    Get all attendance records for a specific session
    
    Only Admin and Instructor can access.
    
    Returns list of attendees with user details.
    """
    # Verify session exists
    try:
        session = await db.sessions.find_one({"_id": ObjectId(session_id)})
        if not session:
            session = await db.sessions.find_one({"_id": session_id})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session ID format"
        )
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Get all attendance records for this session
    attendance_records = await db.attendance_records.find(
        {"session_id": session_id}
    ).to_list(length=None)
    
    # Enrich with user information
    result = []
    for record in attendance_records:
        user = await db.users.find_one({"_id": ObjectId(record["user_id"])})
        if user:
            result.append({
                "attendance_id": str(record["_id"]),
                "user_id": record["user_id"],
                "user_name": user["name"],
                "user_email": user["email"],
                "status": record["status"],
                "method": record["method"],
                "timestamp": record["timestamp"]
            })
    
    return result


# Import for type hint
from utils.auth import require_role
