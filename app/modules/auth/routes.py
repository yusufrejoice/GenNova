from fastapi import APIRouter, Depends, status
from app.modules.auth.schema import UserSignup, UserLogin, TokenResponse, UserProfile
from app.modules.auth.service import signup_user, login_user
from app.modules.auth.dependencies import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup):
    """
    Register a new user or admin.
    """
    return signup_user(user_data)

@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin):
    """
    Log in with email and password.
    """
    return login_user(login_data)

@router.get("/me", response_model=UserProfile)
def get_me(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get the current user's profile.
    """
    return current_user
