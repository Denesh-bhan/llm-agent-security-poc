
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

if not key:
    raise RuntimeError("Gemini API key missing from .env")

client = genai.Client(api_key=key)

print("\nAVAILABLE GEMINI MODELS\n")

try:
    for model in client.models.list():
        actions = getattr(model, "supported_actions", None)

        if actions and "generateContent" not in actions:
            continue

        print("Model:", model.name)
        print("Supported actions:", actions)
        print("-" * 40)

except Exception as error:
    print("Could not list models:", error)
