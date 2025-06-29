from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from services.scheduler import ContentScheduler
from auth import get_current_user

router = APIRouter(prefix="/content", tags=["content"])

class PostCreate(BaseModel):
    account_id: int
    content: str
    media_urls: Optional[List[str]] = None
    scheduled_time: Optional[datetime] = None

class PostResponse(BaseModel):
    id: int
    account_id: int
    content: str
    media_urls: List[str]
    scheduled_time: datetime
    status: str

@router.post("/", response_model=PostResponse)
async def schedule_post(
    post: PostCreate,
    user = Depends(get_current_user)
):
    scheduler = ContentScheduler()
    try:
        scheduled_post = scheduler.schedule_post(
            account_id=post.account_id,
            content=post.content,
            media_urls=post.media_urls,
            scheduled_time=post.scheduled_time
        )
        return scheduled_post
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{account_id}", response_model=List[PostResponse])
async def get_scheduled_posts(
    account_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    user = Depends(get_current_user)
):
    scheduler = ContentScheduler()
    return scheduler.get_scheduled_posts(
        account_id=account_id,
        start_time=start_time,
        end_time=end_time
    )

@router.delete("/{post_id}")
async def cancel_post(
    post_id: int,
    user = Depends(get_current_user)
):
    scheduler = ContentScheduler()
    if not scheduler.cancel_post(post_id):
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post cancelled successfully"}