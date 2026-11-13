
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

if not key:
    raise RuntimeError("Gemini API key not found.")

client = genai.Client(api_key=key)

model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

print("Testing model:", model)

for attempt in range(1, 4):
    try:
        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: GEMINI CONNECTION SUCCESSFUL"
        )

        print("SUCCESS!")
        print("Response:", response.text)
        break

    except Exception as error:
        print(f"Attempt {attempt} failed: {error}")

        if attempt == 3:
            print("Please retry later or check model availability.")
        else:
            wait = attempt * 15
            print(f"Waiting {wait} seconds...")
            time.sleep(wait)
