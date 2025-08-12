import google.generativeai as genai
import os

# Ensure your API key is configured (using environment variable as before)
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# If the environment variable method is still giving you trouble, temporarily hardcode for this script:
# genai.configure(api_key="AIzaSyAE95F3kGk-Ilr4gvhSPkf6iQLk5lR2hRA") # <-- USE YOUR ACTUAL KEY

# REMOVE THIS BLOCK (3 lines):
# if not genai.api_key:
#     print("Error: GOOGLE_API_KEY environment variable not set. Please set it before running this script.")
#     exit()

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