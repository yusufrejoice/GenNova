from typing import Dict, Any, List
from app.database.supabase_client import supabase
from fastapi import HTTPException
from datetime import datetime, timedelta

class AdminService:
    @staticmethod
    def ban_user(user_id: str, days: int) -> Dict[str, Any]:
        """Ban a user for a specific number of days."""
        banned_until = datetime.utcnow() + timedelta(days=days)
        response = supabase.table("profiles").update({
            "banned_until": banned_until.isoformat()
        }).eq("id", user_id).execute()
        
        return {"user_id": user_id, "banned_until": banned_until}

    @staticmethod
    def unban_user(user_id: str) -> Dict[str, Any]:
        """Remove a ban from a user."""
        response = supabase.table("profiles").update({
            "banned_until": None
        }).eq("id", user_id).execute()
        
        return {"user_id": user_id, "status": "unbanned"}

    @staticmethod
    def toggle_model_status(model_id: str, is_active: bool) -> Dict[str, Any]:
        """Enable or disable a model globally."""
        response = supabase.table("app_models").update({
            "is_active": is_active
        }).eq("id", model_id).execute()
        
        return {"model_id": model_id, "is_active": is_active}

    @staticmethod
    def is_model_active(model_id: str) -> bool:
        """Check if a model is currently allowed for use."""
        response = supabase.table("app_models").select("is_active").eq("id", model_id).limit(1).execute()
        if not response or not response.data or len(response.data) == 0:
            # If not in table, assume active but warn
            return True
        return response.data[0].get("is_active", True)

admin_service = AdminService()
