from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database.supabase_client import supabase
from app.modules.auth.service import get_profile_by_id
from typing import Dict, Any

auth_scheme = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> Dict[str, Any]:
    """
    Dependency to verify the Supabase JWT and return the user profile.
    """
    try:
        # Verify the token with Supabase
        user_response = supabase.auth.get_user(token.credentials)
        if not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        # Get custom profile from 'profiles' table
        profile = get_profile_by_id(user_response.user.id)
        
        # Check if user is banned
        banned_until = profile.get("banned_until")
        if banned_until:
            from datetime import datetime
            if datetime.fromisoformat(banned_until.replace('Z', '+00:00')) > datetime.now().astimezone():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User is banned until {banned_until}"
                )
                
        return profile

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

def check_admin_role(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Dependency to restrict access to admin users only.
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def has_sufficient_credits(amount: int = 1):
    """
    Dependency to check if a user has enough credits before an operation.
    """
    def dependency(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_credits = current_user.get("credits", 0)
        if user_credits < amount:
            raise HTTPException(
                status_code=402,
                detail="Insufficient credits. Please contact admin to add credits."
            )
        return current_user
    return dependency
