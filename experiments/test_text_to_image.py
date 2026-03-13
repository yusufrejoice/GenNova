import requests
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_wavespeed_image():
    # Use a faster model for testing
    model_id = "wavespeed-ai/flux-dev-lora-ultra-fast"
    api_key = settings.WAVESPEED_API_KEY
    
    if not api_key:
        print("Error: WAVESPEED_API_KEY not found in environment")
        return

    url = f"https://api.wavespeed.ai/api/v3/{model_id}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": "a majestic lion in the savannah, cinematic lighting",
        "guidance_scale": 3.5,
        "num_inference_steps": 25,
        "width": 1024,
        "height": 1024,
        "enable_base64_output": False
    }

    print(f"Sending request to WaveSpeed for model: {model_id}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=90)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Successfully received response:")
            print(data)
            
            # Extract the actual URL from outputs
            result_data = data.get("data", {})
            outputs = result_data.get("outputs", [])
            if outputs:
                print(f"Success! Final Image URL: {outputs[0]}")
            else:
                print("Generation started but no outputs yet (Async response).")
                print(f"Check status at: {result_data.get('urls', {}).get('get')}")
        else:
            print(f"Failed! Error: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")

if __name__ == "__main__":
    test_wavespeed_image()
