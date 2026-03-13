import logging
from fastapi import HTTPException, status
from app.database.supabase_client import supabase
from app.core.email_service import send_welcome_email
from app.modules.auth.schema import UserSignup, UserLogin, UserProfile
from typing import Dict, Any

logger = logging.getLogger(__name__)

def signup_user(user_data: UserSignup) -> Dict[str, Any]:
    """
    Handles user signup:
    1. Sign up user via Supabase Auth.
    2. Create corresponding profile in the 'profiles' table.
    3. Send welcome email.
    """
    try:
        # 1. Supabase Auth Signup
        # Note: Ensure "Confirm email" is DISABLED in Supabase Dashboard -> Auth -> Providers -> Email
        # This will automatically mark the email as confirmed upon signup.
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })

        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signup failed - check Supabase logs"
            )

        user_id = response.user.id

        # 2. Insert profile
        profile_data = {
            "id": user_id,
            "name": user_data.name,
            "email": user_data.email,
            "role": user_data.role
        }
        
        profile_response = supabase.table("profiles").insert(profile_data).execute()
        
        # 3. Send custom SMTP welcome email (GenNova branded)
        send_welcome_email(user_data.email, user_data.name, user_data.role)
        
        return {
            "message": "User registered successfully",
            "user": profile_response.data[0]
        }

    except Exception as e:
        logger.error(f"Signup error: {e}")
        # Cleanup: In production, you might want to delete the auth user if profile creation fails
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def login_user(login_data: UserLogin) -> Dict[str, Any]:
    """
    Handles user login via Supabase Auth and returns JWT + profile.
    """
    try:
        # 1. Sign in with password
        response = supabase.auth.sign_in_with_password({
            "email": login_data.email,
            "password": login_data.password
        })
        
        if not response.session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        # 2. Get profile
        response_profile = supabase.table("profiles").select("*").eq("id", response.user.id).limit(1).execute()
        
        if not response_profile or not response_profile.data or len(response_profile.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found"
            )

        return {
            "access_token": response.session.access_token,
            "user": response_profile.data[0]
        }

    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

def get_profile_by_id(user_id: str) -> Dict[str, Any]:
    """
    Retrieves user profile from database.
    """
    profile_response = supabase.table("profiles").select("*").eq("id", user_id).limit(1).execute()
    if not profile_response or not profile_response.data or len(profile_response.data) == 0:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile_response.data[0]
