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
    
    print(f"✓ Response received!")
    print(f"Response type: {type(response).__name__}")
    print(f"Has 'text' attr: {hasattr(response, 'text')}")
    print(f"Has 'candidates' attr: {hasattr(response, 'candidates')}")
    print(f"Has 'parts' attr: {hasattr(response, 'parts')}")
    
    if hasattr(response, 'text'):
        print(f"\n✓ SUCCESS! Summary: {response.text}")
    elif hasattr(response, 'candidates') and response.candidates:
        print(f"\nCandidates found: {len(response.candidates)}")
        for idx, candidate in enumerate(response.candidates):
            print(f"\nCandidate {idx}:")
            print(f"  Type: {type(candidate).__name__}")
            print(f"  Has content: {hasattr(candidate, 'content')}")
            if hasattr(candidate, 'content'):
                print(f"  Content type: {type(candidate.content).__name__}")
                print(f"  Has parts: {hasattr(candidate.content, 'parts')}")
                if hasattr(candidate.content, 'parts'):
                    print(f"  Number of parts: {len(candidate.content.parts)}")
                    for pidx, part in enumerate(candidate.content.parts):
                        if hasattr(part, 'text'):
                            print(f"    Part {pidx} text: {part.text}")
    else:
        print("\n⚠ Warning: Could not extract text from response")
        print(f"Response: {response}")
    
    print("\n" + "="*60)
    print("Test Complete")
    print("="*60)

except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
