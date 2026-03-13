from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from app.modules.auth.dependencies import check_admin_role
from app.modules.admin.credit_service import credit_service
from app.modules.admin.admin_service import admin_service
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin Control"])

class CreditUpdate(BaseModel):
    user_id: str
    amount: int

class UserBanRequest(BaseModel):
    user_id: str
    days: int

class ModelStatusUpdate(BaseModel):
    model_id: str
    is_active: bool

@router.post("/credits/add")
async def add_credits(
    request: CreditUpdate,
    admin: Dict[str, Any] = Depends(check_admin_role)
):
    try:
        return credit_service.add_credits(request.user_id, request.amount)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users/ban")
async def ban_user(
    request: UserBanRequest,
    admin: Dict[str, Any] = Depends(check_admin_role)
):
    try:
        return admin_service.ban_user(request.user_id, request.days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/users/unban/{user_id}")
async def unban_user(
    user_id: str,
    admin: Dict[str, Any] = Depends(check_admin_role)
):
    try:
        return admin_service.unban_user(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/toggle")
async def toggle_model(
    request: ModelStatusUpdate,
    admin: Dict[str, Any] = Depends(check_admin_role)
):
    try:
        return admin_service.toggle_model_status(request.model_id, request.is_active)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
