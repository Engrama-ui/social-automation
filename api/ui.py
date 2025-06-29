from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/ui", tags=["ui"])

@router.get("/", response_class=HTMLResponse)
async def get_ui():
    with open("templates/index.html", "r") as f:
        return HTMLResponse(content=f.read())