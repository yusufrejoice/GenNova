import os
import requests
import json
import sys
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def test_wavespeed_generation():
    """
    GenNova Multi-Model Image Tester using WaveSpeed API.
    Supports Flux, Schnell, Ghibli, and SDXL models.
    """
    
    # 1. Terminal Header
    print("\n=== GenNova Multi-Model Image Tester ===")
    
    # 2. Load API Key
    api_key = os.getenv("WAVESPEED_API_KEY")
    if not api_key:
        print("\n[ERROR] WAVESPEED_API_KEY environment variable not found in .env")
        sys.exit(1)

    # 3. Model Selection
    models = {
        "1": "wavespeed-ai/flux-dev-lora-ultra-fast",
        "2": "wavespeed-ai/flux-schnell",
        "3": "wavespeed-ai/flux-dev",
        "4": "wavespeed-ai/flux-schnell-lora",
        "5": "wavespeed-ai/flux-dev-lora"
    }

    print("\nSelect a model:")
    for key, name in models.items():
        print(f"{key}. {name}")
    
    choice = input("\nEnter choice (1-5) [Default 1]: ").strip() or "1"
    target_model = models.get(choice, models["1"])

    # 4. User Input
    print(f"\nUsing Model: {target_model}")
    print("Enter prompt:")
    prompt = input("> ").strip()
    
    if not prompt:
        print("[ERROR] Prompt cannot be empty.")
        return

    # 5. API Configuration
    # Note: Broad endpoint that handles multiple models via URL or payload
    url = f"https://api.wavespeed.ai/api/v3/{target_model}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": prompt,
        "guidance_scale": 3.5,
        "enable_base64_output": False
    }

    print(f"\nGenerating image with {target_model}...")
    
    # 6. Send POST Request
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        response.raise_for_status()
        
        print("\n--- API Response (JSON) ---")
        print(json.dumps(response.json(), indent=4))
        print(f"\nSuccess! Results received for model: {target_model}")

    except Exception as err:
        print(f"\n[ERROR] {err}")
        if 'response' in locals():
            try:
                print(json.dumps(response.json(), indent=2))
            except:
                pass

if __name__ == "__main__":
    test_wavespeed_generation()
