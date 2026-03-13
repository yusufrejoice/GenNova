from pydantic import BaseModel, Field
from typing import Optional

class ProductDescriptionRequest(BaseModel):
    product_name: str = Field(..., example="Wireless Earbuds")
    features: str = Field(..., example="Heavy build quality, noise cancellation")
    model_id: Optional[str] = Field(None, example="meta-llama/Llama-3.1-8B-Instruct")

class BlogRequest(BaseModel):
    topic: str = Field(..., example="The future of AI")
    tone: str = Field(default="professional", example="professional, casual, creative")
    model_id: Optional[str] = Field(None, example="Qwen/Qwen2.5-7B-Instruct")

class CaptionRequest(BaseModel):
    topic: str = Field(..., example="New product launch")
    platform: str = Field(default="Instagram", example="Instagram, Twitter, LinkedIn")
    model_id: Optional[str] = Field(None, example="deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

class RefineRequest(BaseModel):
    original_text: str = Field(..., example="Previous AI output here")
    refinement_instructions: str = Field(..., example="Make it shorter and more professional")
    tool_type: Optional[str] = Field(None, example="caption, blog, product_description")
    model_id: Optional[str] = Field(None, example="meta-llama/Llama-3.1-8B-Instruct")
    parent_id: Optional[str] = Field(None, example="UUID of the original generation")

class ManualEditRequest(BaseModel):
    generation_id: str = Field(..., example="UUID of the generation")
    updated_text: str = Field(..., example="Manually corrected text")
    parent_id: Optional[str] = Field(None, example="UUID of the original generation to link to")

class TextGenerationResponse(BaseModel):
    generated_text: str
    model_used: str
    status: str = "success"
