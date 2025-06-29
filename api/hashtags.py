from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from services.hashtags import HashtagOptimizer
from auth import get_current_user

router = APIRouter(prefix="/hashtags", tags=["hashtags"])

class HashtagResearchResponse(BaseModel):
    hashtag: str
    popularity: float
    related_hashtags: List[str]
    recent_posts: int

class HashtagPerformanceResponse(BaseModel):
    hashtag: str
    total_posts: int
    total_engagement: int
    average_engagement: float

class HashtagSuggestionRequest(BaseModel):
    content: str
    limit: int = 5

@router.get("/research/{hashtag}", response_model=HashtagResearchResponse)
async def research_hashtag(
    hashtag: str,
    user = Depends(get_current_user)
):
    optimizer = HashtagOptimizer()
    try:
        return optimizer.research_hashtag(hashtag)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/performance/{hashtag_id}", response_model=HashtagPerformanceResponse)
async def get_hashtag_performance(
    hashtag_id: int,
    user = Depends(get_current_user)
):
    optimizer = HashtagOptimizer()
    try:
        return optimizer.track_performance(hashtag_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/suggestions", response_model=List[str])
async def get_hashtag_suggestions(
    request: HashtagSuggestionRequest,
    user = Depends(get_current_user)
):
    optimizer = HashtagOptimizer()
    try:
        return optimizer.get_suggestions(request.content, request.limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/trending", response_model=List[Dict])
async def get_trending_hashtags(
    platform: str = "all",
    user = Depends(get_current_user)
):
    optimizer = HashtagOptimizer()
    try:
        return optimizer.get_trending(platform)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))