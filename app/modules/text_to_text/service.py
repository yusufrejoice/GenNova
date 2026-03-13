import os
from huggingface_hub import InferenceClient
from app.core.config import settings
from app.database.supabase_client import supabase
from typing import Dict, Any

class TextToTextService:
    DEFAULT_MODEL = "meta-llama/Llama-3.1-8B-Instruct"
    SUPPORTED_MODELS = [
        "meta-llama/Llama-3.1-8B-Instruct",
        "Qwen/Qwen2.5-7B-Instruct",
        "meta-llama/Llama-3.2-1B-Instruct",
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "Qwen/Qwen2.5-Coder-7B-Instruct"
    ]

    def __init__(self):
        self.token = settings.HF_TOKEN
        self.client = InferenceClient(api_key=self.token)

    async def generate_content(self, prompt: str, model_id: str = None) -> str:
        # Fallback logic: dynamic -> default
        target_model = model_id if model_id else self.DEFAULT_MODEL
        try:
            response = self.client.chat_completion(
                model=target_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.7
            )
            content = response.choices[0].message.content
            if not content or content.strip() == "":
                raise Exception("AI returned empty content. Please try again.")
            return content
        except Exception as e:
            raise Exception(f"AI Generation Error ({target_model}): {str(e)}")

    async def refine_content(self, original_text: str, refinement: str, model_id: str = None) -> str:
        """Takes existing content and refines it based on instructions."""
        refine_prompt = f"Original Text: {original_text}\n\nFeedback: {refinement}\n\nPlease update the text based on this feedback."
        return await self.generate_content(refine_prompt, model_id)

    def save_generation(
        self, 
        user_id: str, 
        tool_type: str, 
        input_data: Dict[str, Any], 
        generated_text: str, 
        model_id: str,
        action_type: str = "generate",
        parent_id: str = None
    ) -> str:
        """Saves the generation result to Supabase and returns the ID."""
        try:
            data = {
                "user_id": user_id,
                "tool_type": tool_type,
                "input_data": input_data,
                "generated_text": generated_text,
                "model_id": model_id,
                "action_type": action_type,
                "parent_id": parent_id
            }
            response = supabase.table("text_generations").insert(data).execute()
            if hasattr(response, 'error') and response.error:
                 raise Exception(f"Database Error: {response.error.message}")
            return response.data[0]["id"]
        except Exception as e:
            print(f"Database Error saving generation: {e}")
            raise Exception(f"Failed to save generation: {str(e)}")

    def update_generation(self, generation_id: str, user_id: str, updated_text: str):
        """Updates an existing generation record (Manual Edit)."""
        try:
            supabase.table("text_generations")\
                .update({"generated_text": updated_text, "action_type": "edit"})\
                .eq("id", generation_id)\
                .eq("user_id", user_id)\
                .execute()
        except Exception as e:
            print(f"Database Error updating generation: {e}")
            raise Exception(f"Failed to update generation: {str(e)}")

    def build_product_prompt(self, product_name: str, features: str) -> str:
        return f"Write a professional and compelling product description for {product_name}. Features: {features}"

    def build_blog_prompt(self, topic: str, tone: str) -> str:
        return f"Write a short, engaging blog post about {topic} in a {tone} tone."

    def build_caption_prompt(self, topic: str, platform: str) -> str:
        return f"Write a catchy {platform} caption about {topic}. Include relevant emojis."

text_to_text_service = TextToTextService()
