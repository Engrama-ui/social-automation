from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List
from pydantic import BaseModel
from services.platforms import PlatformManager
from auth import get_current_user

router = APIRouter(prefix="/platforms", tags=["platforms"])

class ConnectRequest(BaseModel):
    platform: str
    auth_data: Dict

class PostRequest(BaseModel):
    content: str
    media_urls: List[str] = None

@router.post("/connect")
async def connect_account(
    request: ConnectRequest,
    user = Depends(get_current_user)
):
    manager = PlatformManager()
    try:
        return manager.connect_account(request.platform, request.auth_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{account_id}/post")
async def post_content(
    account_id: int,
    request: PostRequest,
    user = Depends(get_current_user)
):
    manager = PlatformManager()
    try:
        return manager.post_content(account_id, request.content, request.media_urls)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{account_id}/insights")
async def get_insights(
    account_id: int,
    user = Depends(get_current_user)
):
    manager = PlatformManager()
    try:
        return manager.get_insights(account_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))