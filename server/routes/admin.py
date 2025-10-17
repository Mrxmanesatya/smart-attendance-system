"""
Admin routes
Handles admin-specific operations like stats, analytics, and user management
"""
from fastapi import APIRouter, HTTPException, status, Depends, Response
from typing import List, Dict, Any
from datetime import datetime, timedelta
from bson import ObjectId
from database import get_database
from models.user import TokenData, UserRole, UserResponse
from utils.auth import require_role
import io
import pandas as pd

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/stats")
async def get_system_stats(
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
) -> Dict[str, Any]:
    """
    Get comprehensive system statistics
    
    Admin only endpoint.
    
    Returns:
    - Total users by role
    - Total sessions (active/inactive)
    - Overall attendance rate
    - Pending miss requests
    - Recent activity
    """
    # Count users by role
    total_users = await db.users.count_documents({})
    admin_count = await db.users.count_documents({"role": "admin"})
    instructor_count = await db.users.count_documents({"role": "instructor"})
    trainee_count = await db.users.count_documents({"role": "trainee"})
    
    # Count sessions
    total_sessions = await db.sessions.count_documents({})
    active_sessions = await db.sessions.count_documents({"active": True})
    inactive_sessions = await db.sessions.count_documents({"active": False})
    
    # Count attendance records
    total_attendance_records = await db.attendance_records.count_documents({})
    
    # Calculate overall attendance rate
    if total_sessions > 0 and total_users > 0:
        expected_attendance = total_sessions * trainee_count
        attendance_rate = (total_attendance_records / expected_attendance * 100) if expected_attendance > 0 else 0
    else:
        attendance_rate = 0
    
    # Count pending miss requests
    pending_requests = await db.miss_requests.count_documents({"status": "pending"})
    
    # Get recent activity (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    recent_sessions = await db.sessions.count_documents({
        "created_at": {"$gte": seven_days_ago}
    })
    
    recent_attendance = await db.attendance_records.count_documents({
        "timestamp": {"$gte": seven_days_ago}
    })
    
    recent_registrations = await db.users.count_documents({
        "created_at": {"$gte": seven_days_ago}
    })
    
    return {
        "users": {
            "total": total_users,
            "admins": admin_count,
            "instructors": instructor_count,
            "trainees": trainee_count
        },
        "sessions": {
            "total": total_sessions,
            "active": active_sessions,
            "inactive": inactive_sessions
        },
        "attendance": {
            "total_records": total_attendance_records,
            "overall_rate": round(attendance_rate, 2)
        },
        "miss_requests": {
            "pending": pending_requests
        },
        "recent_activity": {
            "new_sessions": recent_sessions,
            "new_attendance": recent_attendance,
            "new_users": recent_registrations
        }
    }


@router.get("/analytics/daily-attendance")
async def get_daily_attendance_trends(
    days: int = 30,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
) -> List[Dict[str, Any]]:
    """
    Get daily attendance trends for charts
    
    Returns attendance count per day for the last N days.
    
    - **days**: Number of days to retrieve (default: 30)
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Aggregate attendance by day
    pipeline = [
        {
            "$match": {
                "timestamp": {"$gte": start_date}
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$timestamp"
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    
    results = await db.attendance_records.aggregate(pipeline).to_list(length=None)
    
    # Format results
    return [
        {
            "date": item["_id"],
            "attendance_count": item["count"]
        }
        for item in results
    ]


@router.get("/analytics/absence-report")
async def get_absence_report(
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
) -> List[Dict[str, Any]]:
    """
    Get absence report showing users with low attendance
    
    Returns users sorted by attendance percentage (ascending).
    """
    # Get all trainees
    trainees = await db.users.find({"role": "trainee"}).to_list(length=None)
    
    # Total active sessions
    total_sessions = await db.sessions.count_documents({"active": True})
    
    if total_sessions == 0:
        return []
    
    absence_data = []
    
    for trainee in trainees:
        user_id = str(trainee["_id"])
        
        # Count attendance
        attendance_count = await db.attendance_records.count_documents({"user_id": user_id})
        
        # Calculate percentage
        attendance_percentage = (attendance_count / total_sessions * 100) if total_sessions > 0 else 0
        
        absence_data.append({
            "user_id": user_id,
            "name": trainee["name"],
            "email": trainee["email"],
            "attended": attendance_count,
            "missed": total_sessions - attendance_count,
            "total_sessions": total_sessions,
            "attendance_percentage": round(attendance_percentage, 2)
        })
    
    # Sort by attendance percentage (ascending - worst attendance first)
    absence_data.sort(key=lambda x: x["attendance_percentage"])
    
    return absence_data


@router.get("/analytics/session-summary")
async def get_session_summary(
    current_user: TokenData = Depends(require_role([UserRole.ADMIN, UserRole.INSTRUCTOR])),
    db=Depends(get_database)
) -> List[Dict[str, Any]]:
    """
    Get summary of all sessions with attendance counts
    
    Returns list of sessions with attendance statistics.
    """
    sessions = await db.sessions.find({"active": True}).sort("start_time", -1).to_list(length=None)
    
    summary = []
    
    for session in sessions:
        session_id = str(session["_id"])
        
        # Count attendance for this session
        attendance_count = await db.attendance_records.count_documents({"session_id": session_id})
        
        # Get creator info
        creator = await db.users.find_one({"_id": ObjectId(session["created_by"])})
        
        summary.append({
            "session_id": session_id,
            "title": session["title"],
            "description": session.get("description", ""),
            "start_time": session["start_time"],
            "end_time": session["end_time"],
            "created_by": creator["name"] if creator else "Unknown",
            "attendance_count": attendance_count,
            "created_at": session["created_at"]
        })
    
    return summary


@router.get("/users", response_model=List[UserResponse])
async def list_all_users(
    role: str = None,
    skip: int = 0,
    limit: int = 100,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
):
    """
    List all users with optional role filtering
    
    Admin only.
    
    - **role**: Filter by role (admin/instructor/trainee)
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    query = {}
    if role:
        query["role"] = role
    
    cursor = db.users.find(query).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for user in users:
        user["_id"] = str(user["_id"])
    
    return [UserResponse(**user) for user in users]


@router.patch("/users/{user_id}/role")
async def update_user_role(
    user_id: str,
    new_role: UserRole,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
):
    """
    Update a user's role
    
    Admin only. Allows changing user roles.
    
    - **user_id**: ID of the user to update
    - **new_role**: New role to assign (admin/instructor/trainee)
    """
    # Verify user exists
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update role
    await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"role": new_role.value}}
    )
    
    return {
        "message": "User role updated successfully",
        "user_id": user_id,
        "new_role": new_role.value
    }


@router.get("/export/attendance")
async def export_attendance_csv(
    session_id: str = None,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
):
    """
    Export attendance records to CSV
    
    Admin only.
    
    - **session_id**: Optional filter by session ID
    
    Returns CSV file with attendance data.
    """
    # Build query
    query = {}
    if session_id:
        query["session_id"] = session_id
    
    # Fetch attendance records
    attendance_records = await db.attendance_records.find(query).to_list(length=None)
    
    if not attendance_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No attendance records found"
        )
    
    # Enrich with user and session info
    data = []
    for record in attendance_records:
        user = await db.users.find_one({"_id": ObjectId(record["user_id"])})
        try:
            session = await db.sessions.find_one({"_id": ObjectId(record["session_id"])})
            if not session:
                session = await db.sessions.find_one({"_id": record["session_id"]})
        except:
            session = await db.sessions.find_one({"_id": record["session_id"]})
        
        data.append({
            "Attendance ID": str(record["_id"]),
            "User Name": user["name"] if user else "Unknown",
            "User Email": user["email"] if user else "Unknown",
            "User Role": user["role"] if user else "Unknown",
            "Session Title": session["title"] if session else "Unknown",
            "Session Start": session["start_time"] if session else "Unknown",
            "Status": record["status"],
            "Method": record["method"],
            "Timestamp": record["timestamp"],
            "Organization": user.get("org_name", "") if user else ""
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Convert to CSV
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_content = csv_buffer.getvalue()
    
    # Return as response
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=attendance_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    )


@router.get("/export/attendance-excel")
async def export_attendance_excel(
    session_id: str = None,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
):
    """
    Export attendance records to Excel
    
    Admin only.
    
    - **session_id**: Optional filter by session ID
    
    Returns Excel file with attendance data.
    """
    # Build query
    query = {}
    if session_id:
        query["session_id"] = session_id
    
    # Fetch attendance records
    attendance_records = await db.attendance_records.find(query).to_list(length=None)
    
    if not attendance_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No attendance records found"
        )
    
    # Enrich with user and session info
    data = []
    for record in attendance_records:
        user = await db.users.find_one({"_id": ObjectId(record["user_id"])})
        try:
            session = await db.sessions.find_one({"_id": ObjectId(record["session_id"])})
            if not session:
                session = await db.sessions.find_one({"_id": record["session_id"]})
        except:
            session = await db.sessions.find_one({"_id": record["session_id"]})
        
        data.append({
            "Attendance ID": str(record["_id"]),
            "User Name": user["name"] if user else "Unknown",
            "User Email": user["email"] if user else "Unknown",
            "User Role": user["role"] if user else "Unknown",
            "Session Title": session["title"] if session else "Unknown",
            "Session Start": session["start_time"] if session else "Unknown",
            "Status": record["status"],
            "Method": record["method"],
            "Timestamp": record["timestamp"],
            "Organization": user.get("org_name", "") if user else ""
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Convert to Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Attendance')
    
    excel_content = excel_buffer.getvalue()
    
    # Return as response
    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=attendance_export_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.xlsx"
        }
    )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
):
    """
    Delete a user (soft delete - deactivate)
    
    Admin only.
    
    - **user_id**: ID of the user to delete
    """
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deleting yourself
    current_user_doc = await db.users.find_one({"email": current_user.email})
    if str(current_user_doc["_id"]) == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Delete user (hard delete for now, can be changed to soft delete)
    await db.users.delete_one({"_id": ObjectId(user_id)})
    
    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }
