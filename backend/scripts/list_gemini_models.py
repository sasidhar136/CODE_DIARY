import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure your API key is configured (using environment variable as before)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


print("--- Listing Available Gemini Models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model: {m.name}")
            print(f"  Description: {m.description}")
            print(f"  Supported methods: {m.supported_generation_methods}")
            print("-" * 30)
except Exception as e:
    print(f"An error occurred while listing models: {e}")

print("--- End Model List ---")
