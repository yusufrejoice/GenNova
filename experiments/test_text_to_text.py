import asyncio
import os
from dotenv import load_dotenv
from app.modules.text_to_text.service import text_to_text_service

load_dotenv()

async def test_text_generation():
    print("--- Testing Text-to-Text Generation ---")
    
    # 1. Test Product Description
    print("\n[1] Testing Product Description:")
    product_prompt = text_to_text_service.build_product_prompt(
        "GenNova AI", 
        "multi-modal capabilities, fast generation, intuitive UI"
    )
    try:
        product_desc = await text_to_text_service.generate_content(product_prompt)
        print("Generated Description:")
        print(product_desc)
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test Blog Generation
    print("\n[2] Testing Blog Generation:")
    blog_prompt = text_to_text_service.build_blog_prompt(
        "The Future of AI Art", 
        "enthusiastic"
    )
    try:
        blog_content = await text_to_text_service.generate_content(blog_prompt)
        print("Generated Blog:")
        print(blog_content)
    except Exception as e:
        print(f"Error: {e}")

    # 3. Test Refinement
    if 'product_desc' in locals():
        print("\n[3] Testing Refinement:")
        try:
            refined = await text_to_text_service.refine_content(
                product_desc, 
                "Make it more futuristic and shorter."
            )
            print("Refined Content:")
            print(refined)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_text_generation())
