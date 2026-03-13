from fastapi import APIRouter, HTTPException, Depends
from app.modules.text_to_text.schemas import (
    ProductDescriptionRequest, 
    BlogRequest, 
    CaptionRequest, 
    RefineRequest,
    ManualEditRequest,
    TextGenerationResponse
)
from app.modules.text_to_text.service import text_to_text_service
from app.modules.auth.dependencies import get_current_user
from typing import Dict, Any

router = APIRouter(prefix="/text-to-text", tags=["Text-to-Text AI"])

@router.post("/generate-product-description")
async def generate_product_description(
    request: ProductDescriptionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        model_id = request.model_id or text_to_text_service.DEFAULT_MODEL
        prompt = text_to_text_service.build_product_prompt(request.product_name, request.features)
        content = await text_to_text_service.generate_content(prompt, request.model_id)
        
        gen_id = text_to_text_service.save_generation(
            user_id=current_user["id"],
            tool_type="product_description",
            input_data={"product_name": request.product_name, "features": request.features},
            generated_text=content,
            model_id=model_id,
            action_type="generate"
        )
        
        return {
            "id": gen_id,
            "generated_text": content,
            "model_used": model_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-blog")
async def generate_blog(
    request: BlogRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        model_id = request.model_id or text_to_text_service.DEFAULT_MODEL
        prompt = text_to_text_service.build_blog_prompt(request.topic, request.tone)
        content = await text_to_text_service.generate_content(prompt, request.model_id)
        
        gen_id = text_to_text_service.save_generation(
            user_id=current_user["id"],
            tool_type="blog",
            input_data={"topic": request.topic, "tone": request.tone},
            generated_text=content,
            model_id=model_id,
            action_type="generate"
        )
        
        return {
            "id": gen_id,
            "generated_text": content,
            "model_used": model_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-caption")
async def generate_caption(
    request: CaptionRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        model_id = request.model_id or text_to_text_service.DEFAULT_MODEL
        prompt = text_to_text_service.build_caption_prompt(request.topic, request.platform)
        content = await text_to_text_service.generate_content(prompt, request.model_id)
        
        gen_id = text_to_text_service.save_generation(
            user_id=current_user["id"],
            tool_type="caption",
            input_data={"topic": request.topic, "platform": request.platform},
            generated_text=content,
            model_id=model_id,
            action_type="generate"
        )
        
        return {
            "id": gen_id,
            "generated_text": content,
            "model_used": model_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refine")
async def refine_text(
    request: RefineRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        content = await text_to_text_service.refine_content(
            request.original_text, 
            request.refinement_instructions, 
            request.model_id
        )
        
        # Save refinement as a new history record linked to parent
        model_id = request.model_id or text_to_text_service.DEFAULT_MODEL
        tool_type = request.tool_type or "refine"
        gen_id = text_to_text_service.save_generation(
            user_id=current_user["id"],
            tool_type=tool_type,
            input_data={"original_text": request.original_text, "instructions": request.refinement_instructions},
            generated_text=content,
            model_id=model_id,
            action_type="refine",
            parent_id=request.parent_id
        )
        
        return {
            "id": gen_id,
            "generated_text": content,
            "model_used": model_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/manual-edit")
async def manual_edit(
    request: ManualEditRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        text_to_text_service.update_generation(
            request.generation_id, 
            current_user["id"], 
            request.updated_text
        )
        return {"message": "Generation updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
