import asyncio
import os
import yaml
import litellm
from dotenv import load_dotenv

# Path to the config files in C:\Users\MC\.litellm
CONFIG_DIR = r"C:\Users\MC\.litellm"
ENV_PATH = os.path.join(CONFIG_DIR, ".env")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.yaml")

# Load credentials
load_dotenv(ENV_PATH)

# Load config
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

# Manually ensure env vars are set for LiteLLM
os.environ["DEEPSEEK_API_KEY"] = os.getenv("DEEPSEEK_API_KEY", "")
os.environ["VERTEX_API_KEY"] = os.getenv("VERTEX_API_KEY", "")
os.environ["VERTEXAI_PROJECT"] = os.getenv("VERTEXAI_PROJECT", "")
os.environ["VERTEXAI_LOCATION"] = os.getenv("VERTEXAI_LOCATION", "")

# Initialize Router
router = litellm.Router(model_list=config["model_list"])

async def test_models():
    models_to_test = ["deepseek-v4-pro", "gemini-3.1-pro"]
    
    for model in models_to_test:
        print(f"\n{'='*20}")
        print(f"Testing Model: {model}")
        print(f"{'='*20}")
        
        try:
            # Simple hello world with thinking expectation
            response = await router.acompletion(
                model=model,
                messages=[{
                    "role": "user", 
                    "content": "Perform a quick diagnostic: 1. Say 'Hello World'. 2. State your model version. 3. Confirm if 'thinking' mode is active."
                }],
                # We don't need to pass params here because they are in the config.yaml
                # but we can force them if we want to be sure.
            )
            
            print(f"STATUS: Success")
            print(f"CONTENT:\n{response.choices[0].message.content}")
            
            # Check for reasoning/thinking content
            msg = response.choices[0].message
            if hasattr(msg, 'reasoning_content') and msg.reasoning_content:
                print(f"\nTHINKING DETECTED (length: {len(msg.reasoning_content)} chars)")
                print(f"Reasoning Sample: {msg.reasoning_content[:150]}...")
            else:
                print("\nTHINKING NOT DETECTED in the 'reasoning_content' field.")
                
        except Exception as e:
            print(f"STATUS: FAILED")
            print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_models())
