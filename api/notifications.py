from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
from pydantic import BaseModel
from services.notifications import NotificationManager
from auth import get_current_user, get_current_user_ws

router = APIRouter(prefix="/notifications", tags=["notifications"])

class NotificationResponse(BaseModel):
    id: int
    message: str
    notification_type: str
    timestamp: datetime
    read: bool

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str
):
    user = get_current_user_ws(token)
    if not user:
        await websocket.close(code=1008)
        return
        
    manager = NotificationManager()
    await websocket.accept()
    manager.register(user.id, websocket)
    
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.unregister(user.id, websocket)

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(user = Depends(get_current_user)):
    manager = NotificationManager()
    return manager.get_user_notifications(user.id)

@router.post("/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    user = Depends(get_current_user)
):
    manager = NotificationManager()
    if not manager.mark_as_read(notification_id):
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification marked as read"}