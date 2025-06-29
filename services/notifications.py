import asyncio
from typing import Dict, List
from database import SessionLocal
from models import Notification, User
from websockets import WebSocketServerProtocol

class NotificationManager:
    def __init__(self):
        self.connections: Dict[int, List[WebSocketServerProtocol]] = {}
        
    async def broadcast(self, user_id: int, message: str):
        if user_id in self.connections:
            for websocket in self.connections[user_id]:
                try:
                    await websocket.send_text(message)
                except:
                    self.connections[user_id].remove(websocket)
                    
    def register(self, user_id: int, websocket: WebSocketServerProtocol):
        if user_id not in self.connections:
            self.connections[user_id] = []
        self.connections[user_id].append(websocket)
        
    def unregister(self, user_id: int, websocket: WebSocketServerProtocol):
        if user_id in self.connections:
            self.connections[user_id].remove(websocket)
            
    async def send_notification(
        self,
        user_id: int,
        message: str,
        notification_type: str = "info"
    ):
        notification = Notification(
            user_id=user_id,
            message=message,
            notification_type=notification_type
        )
        session = SessionLocal()
        try:
            session.add(notification)
            session.commit()
        finally:
            session.close()
        
        await self.broadcast(user_id, message)
        
    def get_user_notifications(self, user_id: int) -> List[Notification]:
        return Notification.query.filter_by(user_id=user_id)\
            .order_by(Notification.timestamp.desc())\
            .all()
            
    def mark_as_read(self, notification_id: int) -> bool:
        notification = Notification.query.get(notification_id)
        if notification:
            notification.read = True
            session = SessionLocal()
            try:
                session.add(notification)
                session.commit()
            finally:
                session.close()
            return True
        return False