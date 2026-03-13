import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env
load_dotenv()

# Selectable Models
# Using models with the highest availability and modern Chat API support
MODELS = {
    "1": {"id": "meta-llama/Llama-3.1-8B-Instruct", "name": "Meta Llama 3.1 8B"},
    "2": {"id": "Qwen/Qwen2.5-7B-Instruct", "name": "Alibaba Qwen 2.5 7B"},
    "3": {"id": "meta-llama/Llama-3.2-1B-Instruct", "name": "Meta Llama 3.2 1B"},
    "4": {"id": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B", "name": "DeepSeek R1 Distill"},
    "5": {"id": "Qwen/Qwen2.5-Coder-7B-Instruct", "name": "Qwen 2.5 Coder 7B"}
}

# Get token from .env
HF_TOKEN = os.getenv("HF_TOKEN")

def generate_text(client, model_id, prompt):
    """Generates text using the chat_completion API for maximum stability across providers."""
    try:
        response = client.chat_completion(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"❌ Error with model {model_id}: {e}")
        return None

def main():
    print("\n" + "="*40)
    print("   GenNova Unified Text AI Tester   ")
    print("="*40 + "\n")

    if not HF_TOKEN:
        print("❌ Error: HF_TOKEN not found in .env file.")
        return

    # Select Model
    print("Select AI Model:")
    for key, model in MODELS.items():
        print(f"{key} - {model['name']}")
    
    model_choice = input("\nChoose model (1-5): ").strip()
    if model_choice not in MODELS:
        print("Invalid choice. Exiting.")
        return
    
    selected_model = MODELS[model_choice]
    print(f"\nUsing Model: {selected_model['name']}")

    # Select Tool
    print("\nChoose Tool:")
    print("1 - Product Description Generator")
    print("2 - Blog Generator")
    print("3 - Social Media Caption Generator")

    tool_choice = input("\nEnter option (1-3): ").strip()

    if tool_choice == "1":
        product = input("Enter product name: ")
        features = input("Enter key features: ")
        prompt = f"Write a professional product description for {product}. Features: {features}"
    elif tool_choice == "2":
        topic = input("Enter blog topic: ")
        tone = input("Tone (professional/casual): ")
        prompt = f"Write a short, engaging blog post about {topic} in a {tone} tone."
    elif tool_choice == "3":
        topic = input("Enter caption topic: ")
        platform = input("Platform (Instagram/Twitter): ")
        prompt = f"Write a catchy {platform} caption about {topic}. Include relevant emojis."
    else:
        print("Invalid choice. Exiting.")
        return

    print(f"\n✨ Generating with {selected_model['name']}, please wait...\n")

    # Initialize Client and Generate
    client = InferenceClient(api_key=HF_TOKEN)
    
    current_prompt = prompt
    last_output = generate_text(client, selected_model['id'], current_prompt)

    while True:
        if last_output:
            print("-" * 30)
            print(f"✅ AI OUTPUT ({selected_model['name']}):")
            print("-" * 30)
            print(last_output.strip())
            print("-" * 30)
        else:
            print("Generation failed.")
            break

        print("\nWhat would you like to do next?")
        print("1 - Regenerate (Get a new version)")
        print("2 - Refine (Give feedback to improve)")
        print("3 - Manual Edit (Mock an edit)")
        print("4 - Exit")

        next_action = input("\nEnter option (1-4): ").strip()

        if next_action == "1":
            print("\n🔄 Regenerating...\n")
            last_output = generate_text(client, selected_model['id'], current_prompt)
        elif next_action == "2":
            refinement = input("\nEnter refinement instructions (e.g. 'Make it shorter'): ")
            refine_prompt = f"Original Text: {last_output}\n\nClient Feedback: {refinement}\n\nPlease update the text based on the feedback."
            print("\n✨ Refining...\n")
            last_output = generate_text(client, selected_model['id'], refine_prompt)
        elif next_action == "3":
            print("\n📝 Current output saved for manual editing simulation.")
            manual_text = input("Enter your manual changes: ")
            print(f"\n✅ Manually Updated Text: {manual_text}")
            last_output = manual_text
        elif next_action == "4":
            print("Exiting tool. Goodbye!")
            break
        else:
            print("Invalid option. Staying with current output.")

if __name__ == "__main__":
    main()