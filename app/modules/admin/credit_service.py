from typing import Dict, Any
from app.database.supabase_client import supabase
from fastapi import HTTPException

class CreditService:
    @staticmethod
    def get_user_credits(user_id: str) -> int:
        """Fetch current credits for a user."""
        response = supabase.table("profiles").select("credits").eq("id", user_id).limit(1).execute()
        if not response or not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User profile not found")
        return response.data[0].get("credits", 0)

    @staticmethod
    def deduct_credits(user_id: str, amount: int = 1) -> Dict[str, Any]:
        """Deduct credits from a user after a successful generation."""
        current_credits = CreditService.get_user_credits(user_id)
        
        if current_credits < amount:
            raise HTTPException(status_code=402, detail="Insufficient credits")
        
        new_credits = current_credits - amount
        response = supabase.table("profiles").update({"credits": new_credits}).eq("id", user_id).execute()
        
        return {"user_id": user_id, "remaining_credits": new_credits}

    @staticmethod
    def add_credits(user_id: str, amount: int) -> Dict[str, Any]:
        """Add credits to a user (Admin only)."""
        current_credits = CreditService.get_user_credits(user_id)
        new_credits = current_credits + amount
        
        response = supabase.table("profiles").update({"credits": new_credits}).eq("id", user_id).execute()
        
        return {"user_id": user_id, "new_total_credits": new_credits}

credit_service = CreditService()
