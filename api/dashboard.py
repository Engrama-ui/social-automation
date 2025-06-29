from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/", response_class=HTMLResponse)
async def get_dashboard(user = Depends(get_current_user)):
    with open("templates/dashboard.html", "r") as f:
        return HTMLResponse(content=f.read())