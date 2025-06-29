from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from pydantic import BaseModel
from services.media import MediaManager
from auth import get_current_user

router = APIRouter(prefix="/media", tags=["media"])

class MediaResponse(BaseModel):
    id: int
    filename: str
    mime_type: str
    created_at: datetime

@router.post("/", response_model=MediaResponse)
async def upload_media(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    manager = MediaManager()
    try:
        return manager.save_media(file, user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[MediaResponse])
async def list_media(user = Depends(get_current_user)):
    manager = MediaManager()
    return manager.list_user_media(user.id)

@router.delete("/{media_id}")
async def delete_media(
    media_id: int,
    user = Depends(get_current_user)
):
    manager = MediaManager()
    if not manager.delete_media(media_id):
        raise HTTPException(status_code=404, detail="Media not found")
    return {"message": "Media deleted successfully"}