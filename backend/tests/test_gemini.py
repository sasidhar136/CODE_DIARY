import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("="*60)
print("Testing Gemini API Connection")
print("="*60)

api_key = os.environ.get("GOOGLE_API_KEY")
print(f"API Key: {'***' + api_key[-8:] if api_key else 'NOT FOUND'}")
print(f"API Key Length: {len(api_key) if api_key else 0}")

try:
    genai.configure(api_key=api_key)
    print("✓ API configured successfully")
    
    model = genai.GenerativeModel('models/gemini-2.0-flash-lite')
    print("✓ Model initialized successfully")
    
    test_text = "Today I learned about Python Flask framework and how to create REST APIs."
    print(f"\nTest Input: {test_text}")
    
    print("\nSending request to Gemini...")
    response = model.generate_content(
        f"Summarize this in one sentence: {test_text}",
        generation_config={"max_output_tokens": 100}
    )
    print(f"\nResponse: {response.text}")
except Exception as e:
    print(f"\nAPI Error: {str(e)}")
