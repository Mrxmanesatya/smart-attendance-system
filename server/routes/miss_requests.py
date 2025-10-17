"""
Miss request management routes
Handles trainee requests for missed attendance corrections
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from bson import ObjectId
from database import get_database
from models.miss_request import (
    MissRequestCreate,
    MissRequestUpdate,
    MissRequestResponse,
    MissRequestInDB,
    RequestStatus
)
from models.user import TokenData, UserRole
from utils.auth import get_current_user, require_role

router = APIRouter(prefix="/api/miss-requests", tags=["Miss Requests"])


@router.post("/", response_model=MissRequestResponse, status_code=status.HTTP_201_CREATED)
async def raise_miss_request(
    request_data: MissRequestCreate,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Raise a missed attendance correction request
    
    Trainees can request attendance correction for sessions they missed.
    
    - **session_id**: ID of the session
    - **reason**: Reason for missing the session (min 10 characters)
    """
    # Verify session exists
    try:
        session = await db.sessions.find_one({"_id": ObjectId(request_data.session_id)})
        if not session:
            session = await db.sessions.find_one({"_id": request_data.session_id})
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
    
    # Get user ID
    user = await db.users.find_one({"email": current_user.email})
    user_id = str(user["_id"])
    
    # Check if attendance already marked for this session
    existing_attendance = await db.attendance_records.find_one({
        "session_id": request_data.session_id,
        "user_id": user_id
    })
    
    if existing_attendance:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attendance already marked for this session"
        )
    
    # Check if request already exists for this session
    existing_request = await db.miss_requests.find_one({
        "session_id": request_data.session_id,
        "user_id": user_id
    })
    
    if existing_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request already submitted for this session"
        )
    
    # Create miss request
    miss_request_dict = request_data.model_dump()
    miss_request_dict["user_id"] = user_id
    
    miss_request_in_db = MissRequestInDB(**miss_request_dict)
    
    # Insert into database
    result = await db.miss_requests.insert_one(miss_request_in_db.model_dump())
    
    # Retrieve created request
    created_request = await db.miss_requests.find_one({"_id": result.inserted_id})
    created_request["_id"] = str(created_request["_id"])
    
    return MissRequestResponse(**created_request)


@router.get("/", response_model=List[MissRequestResponse])
async def list_miss_requests(
    status_filter: RequestStatus = None,
    skip: int = 0,
    limit: int = 50,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    List miss requests
    
    - Trainees see only their own requests
    - Admins and Instructors see all requests
    
    - **status_filter**: Filter by request status (pending/approved/rejected)
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    # Get current user's ID
    user = await db.users.find_one({"email": current_user.email})
    user_id = str(user["_id"])
    
    # Build query
    query = {}
    
    # Role-based filtering
    if current_user.role == UserRole.TRAINEE.value:
        query["user_id"] = user_id
    
    # Status filtering
    if status_filter:
        query["status"] = status_filter.value
    
    # Fetch requests
    cursor = db.miss_requests.find(query).sort("created_at", -1).skip(skip).limit(limit)
    requests = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for req in requests:
        req["_id"] = str(req["_id"])
    
    return [MissRequestResponse(**req) for req in requests]


@router.get("/{request_id}", response_model=MissRequestResponse)
async def get_miss_request(
    request_id: str,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Get details of a specific miss request
    
    Users can view their own requests.
    Admins and Instructors can view any request.
    """
    # Get request
    try:
        request = await db.miss_requests.find_one({"_id": ObjectId(request_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request ID format"
        )
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Get current user's ID
    user = await db.users.find_one({"email": current_user.email})
    user_id = str(user["_id"])
    
    # Permission check
    if (current_user.role == UserRole.TRAINEE.value 
        and request["user_id"] != user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this request"
        )
    
    request["_id"] = str(request["_id"])
    return MissRequestResponse(**request)


@router.patch("/{request_id}", response_model=MissRequestResponse)
async def update_miss_request(
    request_id: str,
    update_data: MissRequestUpdate,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN])),
    db=Depends(get_database)
):
    """
    Approve or reject a miss request (Admin only)
    
    - **status**: New status (approved/rejected)
    - **admin_response**: Optional response message from admin
    
    If approved, creates an attendance record with method "admin_override".
    """
    # Get request
    try:
        request = await db.miss_requests.find_one({"_id": ObjectId(request_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request ID format"
        )
    
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    # Check if request is already processed
    if request["status"] != RequestStatus.PENDING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request has already been processed"
        )
    
    # Update request
    update_dict = update_data.model_dump()
    update_dict["updated_at"] = datetime.utcnow()
    
    await db.miss_requests.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": update_dict}
    )
    
    # If approved, create attendance record
    if update_data.status == RequestStatus.APPROVED:
        from models.attendance import AttendanceInDB, AttendanceStatus, AttendanceMethod
        
        # Check if attendance doesn't already exist
        existing_attendance = await db.attendance_records.find_one({
            "session_id": request["session_id"],
            "user_id": request["user_id"]
        })
        
        if not existing_attendance:
            attendance_record = AttendanceInDB(
                session_id=request["session_id"],
                user_id=request["user_id"],
                status=AttendanceStatus.PRESENT,
                method=AttendanceMethod.ADMIN_OVERRIDE
            )
            
            await db.attendance_records.insert_one(attendance_record.model_dump())
    
    # Retrieve updated request
    updated_request = await db.miss_requests.find_one({"_id": ObjectId(request_id)})
    updated_request["_id"] = str(updated_request["_id"])
    
    return MissRequestResponse(**updated_request)


@router.get("/user/{user_id}/requests", response_model=List[MissRequestResponse])
async def get_user_miss_requests(
    user_id: str,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Get all miss requests for a specific user
    
    Users can view their own requests.
    Admins and Instructors can view anyone's requests.
    """
    # Get current user's ID
    current_user_doc = await db.users.find_one({"email": current_user.email})
    current_user_id = str(current_user_doc["_id"])
    
    # Permission check
    if (current_user.role == UserRole.TRAINEE.value 
        and user_id != current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view these requests"
        )
    
    # Fetch requests
    requests = await db.miss_requests.find(
        {"user_id": user_id}
    ).sort("created_at", -1).to_list(length=None)
    
    # Convert ObjectId to string
    for req in requests:
        req["_id"] = str(req["_id"])
    
    return [MissRequestResponse(**req) for req in requests]
