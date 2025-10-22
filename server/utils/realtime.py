"""
Realtime connection manager for websocket subscriptions.
Manages subscribers by session and broadcasts events.
"""
from typing import Dict, Set, Any
from starlette.websockets import WebSocket
import asyncio


class RealtimeManager:
    def __init__(self) -> None:
        # session_id -> set of websockets
        self._session_subscribers: Dict[str, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, session_id: str) -> None:
        await websocket.accept()
        async with self._lock:
            if session_id not in self._session_subscribers:
                self._session_subscribers[session_id] = set()
            self._session_subscribers[session_id].add(websocket)

    async def disconnect(self, websocket: WebSocket, session_id: str) -> None:
        async with self._lock:
            subscribers = self._session_subscribers.get(session_id)
            if subscribers and websocket in subscribers:
                subscribers.remove(websocket)
            if subscribers is not None and len(subscribers) == 0:
                self._session_subscribers.pop(session_id, None)

    async def broadcast(self, session_id: str, event: str, payload: Any) -> None:
        # Copy to avoid mutation during iteration
        subscribers = list(self._session_subscribers.get(session_id, set()))
        for ws in subscribers:
            try:
                await ws.send_json({"event": event, "data": payload})
            except Exception:
                # Best-effort: cleanup broken sockets
                try:
                    await self.disconnect(ws, session_id)
                except Exception:
                    pass


realtime_manager = RealtimeManager()


