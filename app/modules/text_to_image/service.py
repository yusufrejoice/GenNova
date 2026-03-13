import requests
from typing import Dict, Any
from app.core.config import settings
from app.database.supabase_client import supabase
import logging
import time
from uuid import uuid4

logger = logging.getLogger(__name__)

class TextToImageService:
    def __init__(self):
        self.api_key = settings.WAVESPEED_API_KEY
        self.base_url = "https://api.wavespeed.ai/api/v3"

    def generate_image(self, prompt: str, model_id: str, user_id: str, **kwargs) -> Dict[str, Any]:
        if not self.api_key:
            raise Exception("WaveSpeed API Key not configured")

        url = f"{self.base_url}/{model_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "guidance_scale": 3.5,
            "enable_base64_output": False
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=90)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 200:
                result = data.get("data", {})
                # Polling logic: Wait for 'outputs' to be populated or status to be 'completed'
                actual_image_url = None
                poll_url = result.get("urls", {}).get("get")
                
                if poll_url:
                    logger.info(f"Asynchronous response received. Polling URL: {poll_url}")
                    start_time = time.time()
                    timeout = 30  # Max wait time in seconds
                    
                    while (time.time() - start_time) < timeout:
                        try:
                            # Pass headers with Bearer token for status check
                            poll_res = requests.get(poll_url, headers=headers, timeout=20)
                            poll_res.raise_for_status()
                            poll_data = poll_res.json().get("data", {})
                            
                            status = poll_data.get("status")
                            curr_outputs = poll_data.get("outputs", [])
                            
                            if (status == "completed" or status == "succeeded") and curr_outputs:
                                actual_image_url = curr_outputs[0]
                                logger.info("Image generation completed.")
                                break
                            elif status == "failed":
                                logger.error(f"Image generation failed on API side: {poll_data.get('error')}")
                                break
                                
                            logger.info(f"Generation in progress (status: {status}). Waiting 2 seconds...")
                            time.sleep(2)
                        except Exception as poll_err:
                            logger.error(f"Polling error: {str(poll_err)}")
                            break
                
                # If polling failed to find an image but we had an initial output (unlikely but safe)
                if not actual_image_url and outputs:
                    actual_image_url = outputs[0]
                
                wavespeed_result_url = poll_url
                
                # Logic: Download and Upload to Supabase Storage
                supabase_url = None
                bucket_path = None
                
                if actual_image_url:
                    try:
                        # Download the image
                        logger.info(f"Downloading actual image: {actual_image_url}")
                        img_response = requests.get(actual_image_url, timeout=30)
                        img_response.raise_for_status()
                        
                        # Prepare path: user_id/timestamp_prompt.png
                        ext = "png"
                        if ".jpeg" in actual_image_url.lower() or ".jpg" in actual_image_url.lower():
                            ext = "jpg"
                            
                        filename = f"{int(time.time())}_{uuid4().hex[:8]}.{ext}"
                        bucket_path = f"{user_id}/{filename}"
                        
                        # Upload to Supabase Bucket 'generated-images'
                        logger.info(f"Uploading image to Supabase bucket 'generated-images': {bucket_path}")
                        supabase.storage.from_("generated-images").upload(
                            path=bucket_path,
                            file=img_response.content,
                            file_options={"content-type": f"image/{ext if ext != 'jpg' else 'jpeg'}"}
                        )
                        
                        # Get public URL
                        public_url_res = supabase.storage.from_("generated-images").get_public_url(bucket_path)
                        if isinstance(public_url_res, str):
                            supabase_url = public_url_res
                        else:
                            supabase_url = getattr(public_url_res, "public_url", str(public_url_res))
                            
                        logger.info(f"Successfully uploaded to Supabase. Public URL: {supabase_url}")
                    except Exception as storage_err:
                        logger.error(f"Storage upload failed: {str(storage_err)}")
                        # Fallback to actual image URL if storage fails
                        supabase_url = actual_image_url

                # Save to database
                db_record = self.save_generation(
                    user_id=user_id,
                    prompt=prompt,
                    model_id=model_id,
                    image_url=supabase_url or actual_image_url or wavespeed_result_url,
                    bucket_path=bucket_path,
                    parent_id=kwargs.get("parent_id")
                )
                
                return {
                    "id": db_record.get("id"),
                    "image_url": supabase_url or actual_image_url or wavespeed_result_url,
                    "model_used": model_id,
                    "status": "success",
                    "message": "Image generated and saved successfully"
                }
            else:
                raise Exception(f"API Error: {data.get('message')}")

        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            raise e

    def regenerate_image(self, generation_id: str, user_id: str) -> Dict[str, Any]:
        """Runs the generation again with the same parameters."""
        # 1. Fetch the original generation
        response = supabase.table("image_generations").select("*").eq("id", generation_id).eq("user_id", user_id).execute()
        if not response.data:
            raise Exception("Original generation not found")
        
        original = response.data[0]
        
        # 2. Re-run generation
        return self.generate_image(
            prompt=original["prompt"],
            model_id=original["model_id"],
            user_id=user_id,
            parent_id=generation_id
        )

    def refine_image(self, generation_id: str, refinement: str, user_id: str) -> Dict[str, Any]:
        """Combines original prompt with new instructions for a refined image."""
        # 1. Fetch the original generation
        response = supabase.table("image_generations").select("*").eq("id", generation_id).eq("user_id", user_id).execute()
        if not response.data:
            raise Exception("Original generation not found")
        
        original = response.data[0]
        
        # 2. Build refined prompt
        refined_prompt = f"{original['prompt']}, {refinement}"
        
        # 3. Re-run generation
        return self.generate_image(
            prompt=refined_prompt,
            model_id=original["model_id"],
            user_id=user_id,
            parent_id=generation_id
        )

    # --- Specialized Generators ---

    def generate_product_image(self, product_name: str, category: str, background: str, features: str, user_id: str, model_id: str) -> Dict[str, Any]:
        prompt = f"Professional commercial photography of {product_name}, a {category}. Features: {features}. Background: {background}. High-end lighting, 8k resolution, studio quality, sharp focus."
        return self.generate_image(prompt, model_id, user_id)

    def generate_style_image(self, original_prompt: str, style_name: str, user_id: str, model_id: str) -> Dict[str, Any]:
        style_prompts = {
            "Cinematic": "cinematic lighting, dramatic shadows, movie still, highly detailed",
            "Anime": "anime style, vibrant colors, expressive characters, high-quality digital art",
            "3D Render": "octane render, 3D masterpiece, unreal engine 5, hyper-realistic, volumetric lighting",
            "Oil Painting": "traditional oil painting on canvas, visible brushstrokes, classic art style",
            "Minimalist": "minimalist art, clean lines, simple composition, elegant, modern",
            "Cyberpunk": "cyberpunk aesthetic, neon lights, futuristic, rainy city, high-tech vibe"
        }
        style_suffix = style_prompts.get(style_name, style_name)
        prompt = f"{original_prompt}, {style_suffix}"
        return self.generate_image(prompt, model_id, user_id)

    def generate_character_image(self, gender: str, age: str, hair: str, outfit: str, personality: str, user_id: str, model_id: str) -> Dict[str, Any]:
        prompt = f"A full body portrait of a {age} {gender} with {hair} hair. Wearing {outfit}. Personality: {personality}. Concept art style, highly detailed features, character design sheet quality."
        return self.generate_image(prompt, model_id, user_id)

    def generate_interior_image(self, room_type: str, style: str, user_id: str, model_id: str) -> Dict[str, Any]:
        prompt = f"Interior design of a {room_type}, {style} style. Professional architectural photography, natural lighting, elegant furniture, cozy atmosphere, wide angle shot."
        return self.generate_image(prompt, model_id, user_id)

    def generate_fashion_image(self, item_type: str, material: str, color: str, mood: str, user_id: str, model_id: str) -> Dict[str, Any]:
        prompt = f"A high-fashion shot of a {color} {item_type} made of {material}. Mood: {mood}. Vogue style photography, editorial lighting, detailed texture, sharp focus."
        return self.generate_image(prompt, model_id, user_id)

    def save_generation(self, user_id: str, prompt: str, model_id: str, image_url: str, bucket_path: str = None, parent_id: str = None) -> Dict[str, Any]:
        data = {
            "user_id": user_id,
            "prompt": prompt,
            "model_id": model_id,
            "image_url": image_url,
            "bucket_path": bucket_path,
            "status": "success",
            "parent_id": parent_id
        }
        
        response = supabase.table("image_generations").insert(data).execute()
        
        if hasattr(response, 'data') and len(response.data) > 0:
            return response.data[0]
        else:
            raise Exception("Failed to save image generation history")

text_to_image_service = TextToImageService()
