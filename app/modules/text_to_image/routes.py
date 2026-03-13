from fastapi import APIRouter, HTTPException, Depends
from app.modules.text_to_image.schemas import (
    ImageGenerationRequest, 
    ImageGenerationResponse,
    RegenerateRequest,
    RefineRequest,
    ProductImageRequest,
    StylePresetRequest,
    CharacterRequest,
    InteriorRequest,
    FashionRequest
)
from app.modules.text_to_image.service import text_to_image_service
from app.modules.auth.dependencies import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/image", tags=["Text-to-Image AI"])

@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageGenerationRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")
        result = text_to_image_service.generate_image(
            prompt=request.prompt,
            model_id=request.model_id,
            user_id=user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/regenerate", response_model=ImageGenerationResponse)
async def regenerate_image(
    request: RegenerateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")
        result = text_to_image_service.regenerate_image(
            generation_id=request.generation_id,
            user_id=user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refine", response_model=ImageGenerationResponse)
async def refine_image(
    request: RefineRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")
        result = text_to_image_service.refine_image(
            generation_id=request.generation_id,
            refinement=request.refinement_prompt,
            user_id=user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/product", response_model=ImageGenerationResponse)
async def generate_product_image(
    request: ProductImageRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")
        result = text_to_image_service.generate_product_image(
            product_name=request.product_name,
            category=request.category,
            background=request.background,
            features=request.features,
            user_id=user_id,
            model_id=request.model_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/style", response_model=ImageGenerationResponse)
async def generate_style_image(
    request: StylePresetRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")
        result = text_to_image_service.generate_style_image(
            original_prompt=request.prompt,
            style_name=request.style_name,
            user_id=user_id,
            model_id=request.model_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/character", response_model=ImageGenerationResponse)
async def generate_character_image(
    request: CharacterRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")
        result = text_to_image_service.generate_character_image(
            gender=request.gender,
            age=request.age,
            hair=request.hair_color,
            outfit=request.outfit,
            personality=request.personality,
            user_id=user_id,
            model_id=request.model_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interior", response_model=ImageGenerationResponse)
async def generate_interior_image(
    request: InteriorRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")
        result = text_to_image_service.generate_interior_image(
            room_type=request.room_type,
            style=request.style,
            user_id=user_id,
            model_id=request.model_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/fashion", response_model=ImageGenerationResponse)
async def generate_fashion_image(
    request: FashionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        user_id = current_user.get("id")
        result = text_to_image_service.generate_fashion_image(
            item_type=request.item_type,
            material=request.material,
            color=request.color,
            mood=request.mood,
            user_id=user_id,
            model_id=request.model_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
