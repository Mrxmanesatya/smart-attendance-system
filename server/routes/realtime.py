"""
Realtime routes for websocket attendance updates and live stats polling.
"""
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from typing import Dict, Any
from bson import ObjectId
from database import get_database
from models.user import TokenData, UserRole
from utils.auth import get_current_user, require_role
from utils.realtime import realtime_manager


router = APIRouter(prefix="/api/realtime", tags=["Realtime"])


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for subscribing to live attendance updates of a session.
    Client connects: ws://<host>/api/realtime/ws?session_id=<id>
    """
    # Accept and register connection
    await realtime_manager.connect(websocket, session_id)
    try:
        # Keep the connection alive; we don't expect incoming messages.
        while True:
            # Receive ping/keepalive or ignore incoming payloads
            await websocket.receive_text()
    except WebSocketDisconnect:
        await realtime_manager.disconnect(websocket, session_id)
    except Exception:
        await realtime_manager.disconnect(websocket, session_id)


@router.get("/session/{session_id}/live")
async def get_session_live_stats(
    session_id: str,
    current_user: TokenData = Depends(require_role([UserRole.ADMIN, UserRole.INSTRUCTOR])),
    db=Depends(get_database)
):
    """
    Returns live stats for a session: total students (enrolled), present, absent, late, percentage, and recent scans.
    This is a polling-friendly companion to the websocket.
    """
    # Validate session exists
    try:
        session = await db.sessions.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid session ID format")
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    # Determine cohort size. If enrollment isn't modeled, use total users with role trainee as proxy.
    total_students = await db.users.count_documents({"role": UserRole.TRAINEE.value})

    # Compute attendance for this session
    records = await db.attendance_records.find({"session_id": session_id}).to_list(length=None)
    present = sum(1 for r in records if r.get("status") in ("present", "late"))
    late = sum(1 for r in records if r.get("status") == "late")
    absent = max(total_students - present, 0)
    percentage = round((present / total_students * 100) if total_students else 0, 2)

    # Recent scans (latest 10)
    recent_cursor = db.attendance_records.find({"session_id": session_id}).sort("timestamp", -1).limit(10)
    recent = await recent_cursor.to_list(length=10)
    # Enrich with user name/email
    recent_enriched = []
    for r in recent:
        try:
            user = await db.users.find_one({"_id": ObjectId(r["user_id"])})
        except Exception:
            user = None
        recent_enriched.append({
            "id": str(r.get("_id")),
            "user_id": r.get("user_id"),
            "user_name": user.get("name") if user else None,
            "user_email": user.get("email") if user else None,
            "status": r.get("status"),
            "method": r.get("method"),
            "timestamp": r.get("timestamp"),
        })

    return {
        "session": {"id": str(session.get("_id")), "title": session.get("title"), "active": session.get("active", False)},
        "stats": {
            "total_students": total_students,
            "present": present,
            "absent": absent,
            "late": late,
            "percentage": percentage,
        },
        "recent_scans": recent_enriched,
    }


