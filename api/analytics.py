from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from pydantic import BaseModel
from services.analytics import AnalyticsEngine
from auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["analytics"])

class AccountAnalyticsResponse(BaseModel):
    followers: int
    engagement_rate: float
    best_performing_post: Dict
    weekly_growth: Dict

class PostAnalyticsResponse(BaseModel):
    impressions: int
    engagement_rate: float
    hashtag_performance: Dict
    sentiment_analysis: Dict

class ReportRequest(BaseModel):
    period: str = "30d"

@router.get("/account/{account_id}", response_model=AccountAnalyticsResponse)
async def get_account_analytics(
    account_id: int,
    user = Depends(get_current_user)
):
    engine = AnalyticsEngine()
    try:
        return engine.get_account_analytics(account_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/post/{post_id}", response_model=PostAnalyticsResponse)
async def get_post_analytics(
    post_id: int,
    user = Depends(get_current_user)
):
    engine = AnalyticsEngine()
    try:
        return engine.get_post_analytics(post_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/report/{account_id}")
async def generate_report(
    account_id: int,
    request: ReportRequest,
    user = Depends(get_current_user)
):
    engine = AnalyticsEngine()
    try:
        return engine.generate_report(account_id, request.period)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))