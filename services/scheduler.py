from datetime import datetime, timedelta
from typing import List, Optional
from database import SessionLocal
from models import ScheduledPost

class ContentScheduler:
    def __init__(self):
        self.queue = []
        
    def schedule_post(
        self,
        account_id: int,
        content: str,
        media_urls: Optional[List[str]] = None,
        scheduled_time: Optional[datetime] = None
    ) -> ScheduledPost:
        # Default to 1 hour from now if no time specified
        if not scheduled_time:
            scheduled_time = datetime.now() + timedelta(hours=1)
            
        post = ScheduledPost(
            account_id=account_id,
            content=content,
            media_urls=media_urls or [],
            scheduled_time=scheduled_time
        )
        
        db.session.add(post)
        db.session.commit()
        
        self.queue.append(post)
        return post
        
    def get_scheduled_posts(
        self,
        account_id: int,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[ScheduledPost]:
        query = ScheduledPost.query.filter_by(account_id=account_id)
        
        if start_time:
            query = query.filter(ScheduledPost.scheduled_time >= start_time)
        if end_time:
            query = query.filter(ScheduledPost.scheduled_time <= end_time)
            
        return query.order_by(ScheduledPost.scheduled_time).all()
        
    def cancel_post(self, post_id: int) -> bool:
        post = ScheduledPost.query.get(post_id)
        if post:
            db.session.delete(post)
            db.session.commit()
            return True
        return False
        
    def process_queue(self):
        now = datetime.now()
        posts_to_publish = [
            post for post in self.queue
            if post.scheduled_time <= now
        ]
        
        for post in posts_to_publish:
            self.publish_post(post)
            self.queue.remove(post)
            
    def publish_post(self, post: ScheduledPost):
        # Implementation for publishing to social platforms
        pass