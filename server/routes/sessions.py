"""
Session management routes
Handles session creation, retrieval, and QR code generation
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from datetime import datetime
from bson import ObjectId
from database import get_database
from models.session import SessionCreate, SessionResponse, SessionInDB
from models.qr_code import QRCodeDisplay, QRCodeInDB
from models.user import TokenData, UserRole
from utils.auth import get_current_user, require_role
from utils.qr_generator import generate_qr_code_value, create_qr_image, get_qr_expiry_time

router = APIRouter(prefix="/api/sessions", tags=["Sessions"])


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session: SessionCreate,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN, UserRole.INSTRUCTOR])),
    db=Depends(get_database)
):
    """
    Create a new training/class session
    
    Only Admin and Instructor roles can create sessions.
    
    - **title**: Session title
    - **description**: Optional session description
    - **start_time**: Session start datetime
    - **end_time**: Session end datetime
    """
    # Validate time range
    if session.end_time <= session.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time"
        )
    
    # Get user document to get user ID
    user = await db.users.find_one({"email": current_user.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create session document
    session_dict = session.model_dump()
    session_dict["created_by"] = str(user["_id"])
    session_dict["qr_code_id"] = None
    session_dict["active"] = True
    
    session_in_db = SessionInDB(**session_dict)
    
    # Insert into database
    result = await db.sessions.insert_one(session_in_db.model_dump())
    
    # Retrieve created session
    created_session = await db.sessions.find_one({"_id": result.inserted_id})
    created_session["_id"] = str(created_session["_id"])
    
    return SessionResponse(**created_session)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Get session details by ID
    
    Requires authentication.
    """
    try:
        session = await db.sessions.find_one({"_id": ObjectId(session_id)})
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
    
    session["_id"] = str(session["_id"])
    return SessionResponse(**session)


@router.get("/", response_model=List[SessionResponse])
async def list_sessions(
    skip: int = 0,
    limit: int = 50,
    active_only: bool = True,
    current_user: TokenData = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    List all sessions with pagination
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **active_only**: Filter by active sessions only
    """
    query = {"active": True} if active_only else {}
    
    # If user is instructor or trainee, optionally filter by relevant sessions
    # For now, show all sessions
    
    cursor = db.sessions.find(query).sort("created_at", -1).skip(skip).limit(limit)
    sessions = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for session in sessions:
        session["_id"] = str(session["_id"])
    
    return [SessionResponse(**session) for session in sessions]


@router.get("/{session_id}/qr", response_model=QRCodeDisplay)
async def get_session_qr_code(
    session_id: str,
    regenerate: bool = False,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN, UserRole.INSTRUCTOR])),
    db=Depends(get_database)
):
    """
    Generate or retrieve QR code for a session
    
    Only Admin and Instructor roles can access QR codes.
    
    - **session_id**: ID of the session
    - **regenerate**: Force regenerate QR code (optional)
    
    Returns base64 encoded QR code image with metadata.
    """
    # Get session
    try:
        session = await db.sessions.find_one({"_id": ObjectId(session_id)})
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
    
    # Check if session has an active QR code
    existing_qr = None
    if session.get("qr_code_id") and not regenerate:
        try:
            existing_qr = await db.qr_codes.find_one({"_id": ObjectId(session["qr_code_id"])})
            
            # Check if QR code is still valid
            if existing_qr and existing_qr["expires_at"] > datetime.utcnow():
                # Return existing QR code
                qr_image = create_qr_image(existing_qr["code_value"])
                
                return QRCodeDisplay(
                    qr_image_base64=qr_image,
                    code_value=existing_qr["code_value"],
                    expires_at=existing_qr["expires_at"],
                    session_id=session_id,
                    session_title=session["title"]
                )
        except:
            pass  # If error, generate new QR code
    
    # Generate new QR code
    qr_code_value = generate_qr_code_value(session_id)
    expires_at = get_qr_expiry_time()
    
    qr_code_in_db = QRCodeInDB(
        session_id=session_id,
        code_value=qr_code_value,
        expires_at=expires_at
    )
    
    # Insert QR code into database
    result = await db.qr_codes.insert_one(qr_code_in_db.model_dump())
    
    # Update session with QR code ID
    await db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"qr_code_id": str(result.inserted_id)}}
    )
    
    # Generate QR code image
    qr_image = create_qr_image(qr_code_value)
    
    return QRCodeDisplay(
        qr_image_base64=qr_image,
        code_value=qr_code_value,
        expires_at=expires_at,
        session_id=session_id,
        session_title=session["title"]
    )


@router.patch("/{session_id}/deactivate")
async def deactivate_session(
    session_id: str,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN, UserRole.INSTRUCTOR])),
    db=Depends(get_database)
):
    """
    Deactivate a session (soft delete)
    
    Only Admin and Instructor who created the session can deactivate it.
    """
    # Get session
    try:
        session = await db.sessions.find_one({"_id": ObjectId(session_id)})
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
    
    # Get current user's ID
    user = await db.users.find_one({"email": current_user.email})
    
    # Check permission: Admin can deactivate any session, Instructor only their own
    if current_user.role != UserRole.ADMIN.value and session["created_by"] != str(user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to deactivate this session"
        )
    
    # Deactivate session
    await db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"active": False}}
    )
    
    return {"message": "Session deactivated successfully", "session_id": session_id}
