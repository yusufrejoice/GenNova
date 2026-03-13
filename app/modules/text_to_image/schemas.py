from pydantic import BaseModel
from typing import Optional, Dict, Any

class ImageGenerationRequest(BaseModel):
    prompt: str
    model_id: str = "wavespeed-ai/flux-dev-lora-ultra-fast"

class ImageGenerationResponse(BaseModel):
    id: str
    image_url: str
    model_used: str
    status: str
    message: str

class RegenerateRequest(BaseModel):
    generation_id: str

class RefineRequest(BaseModel):
    generation_id: str
    refinement_prompt: str

class ProductImageRequest(BaseModel):
    product_name: str
    category: str
    background: Optional[str] = "clean studio background"
    features: Optional[str] = ""
    model_id: str = "wavespeed-ai/flux-dev-lora-ultra-fast"

class StylePresetRequest(BaseModel):
    prompt: str
    style_name: str # e.g., "Cinematic", "Anime", "3D Render", "Oil Painting"
    model_id: str = "wavespeed-ai/flux-dev-lora-ultra-fast"

class CharacterRequest(BaseModel):
    gender: str
    age: str
    hair_color: str
    outfit: str
    personality: Optional[str] = ""
    model_id: str = "wavespeed-ai/flux-dev-lora-ultra-fast"

class InteriorRequest(BaseModel):
    room_type: str
    style: str
    model_id: str = "wavespeed-ai/flux-dev-lora-ultra-fast"

class FashionRequest(BaseModel):
    item_type: str
    material: str
    color: str
    mood: Optional[str] = ""
    model_id: str = "wavespeed-ai/flux-dev-lora-ultra-fast"
