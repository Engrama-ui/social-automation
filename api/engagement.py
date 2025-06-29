from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from services.engagement import EngagementTracker
from auth import get_current_user

router = APIRouter(prefix="/engagement", tags=["engagement"])

class EngagementResponse(BaseModel):
    post_id: int
    likes: int
    comments: int
    shares: int
    sentiment_score: float
    timestamp: datetime

class EngagementSummary(BaseModel):
    total_likes: int
    total_comments: int
    total_shares: int
    average_sentiment: float

@router.get("/post/{post_id}", response_model=EngagementResponse)
async def get_post_engagement(
    post_id: int,
    user = Depends(get_current_user)
):
    tracker = EngagementTracker()
    engagement = tracker.get_engagement_metrics(post_id)
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement data not found")
    return engagement

@router.get("/account/{account_id}/recent", response_model=List[EngagementResponse])
async def get_recent_engagements(
    account_id: int,
    limit: int = 100,
    user = Depends(get_current_user)
):
    tracker = EngagementTracker()
    return tracker.get_recent_engagements(account_id, limit)

@router.get("/account/{account_id}/summary", response_model=EngagementSummary)
async def get_engagement_summary(
    account_id: int,
    user = Depends(get_current_user)
):
    tracker = EngagementTracker()
    try:
        return tracker.get_engagement_summary(account_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))