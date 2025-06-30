from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Optional, List
from pydantic import BaseModel
from services.templates import TemplateManager
from auth import get_current_user

router = APIRouter(prefix="/templates", tags=["templates"])

class TemplateCreate(BaseModel):
    name: str
    content: str
    variables: Optional[Dict[str, str]] = None

class TemplateResponse(BaseModel):
    id: int
    name: str
    content: str
    variables: Dict[str, str]

class TemplateApplyRequest(BaseModel):
    template_id: int
    variables: Dict[str, str]

@router.post("/", response_model=TemplateResponse)
async def create_template(
    template: TemplateCreate,
    user = Depends(get_current_user)
):
    manager = TemplateManager()
    try:
        return manager.create_template(
            name=template.name,
            content=template.content,
            variables=template.variables
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TemplateResponse])
async def list_templates(user = Depends(get_current_user)):
    manager = TemplateManager()
    return manager.list_templates()

@router.post("/apply")
async def apply_template(
    request: TemplateApplyRequest,
    user = Depends(get_current_user)
):
    manager = TemplateManager()
    try:
        return {
            "content": manager.apply_template(
                request.template_id,
                request.variables
            )
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{template_id}")
async def delete_template(
    template_id: int,
    user = Depends(get_current_user)
):
    manager = TemplateManager()
    if not manager.delete_template(template_id):
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template deleted successfully"}