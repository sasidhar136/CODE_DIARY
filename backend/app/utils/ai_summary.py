"""
AI-powered summarization utilities using Google Generative AI
"""
import os
import google.generativeai as genai
from flask import current_app

# Configure Google AI
if os.environ.get('GOOGLE_API_KEY'):
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

def get_ai_summary(text_content):
    """
    Generate an AI summary of the given text using Google Generative AI
    
    Args:
        text_content (str): The text to summarize
        
    Returns:
        str: The generated summary or None if generation failed
    """
    try:
        print(f"\n{'='*50}")
        print(f"Starting AI Summary Generation")
        print(f"{'='*50}")
        print(f"API Key: {'***' + str(os.environ.get('GOOGLE_API_KEY'))[-8:] if os.environ.get('GOOGLE_API_KEY') else 'NOT SET'}")
        print(f"Content length: {len(text_content)} characters")
        
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        print(f"✓ Model initialized")

        prompt = f"Summarize the following technical learning entry concisely (2-3 sentences), focusing on key concepts learned and any technologies mentioned:\n\n{text_content}"
        print(f"Sending request to Gemini API...")
        
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 150}
        )
        
        print(f"✓ API Response received")
        print(f"Response type: {type(response).__name__}")
        
        summary = None

        # Method 1: Try response.text (most direct)
        if hasattr(response, 'text') and response.text:
            summary = response.text.strip()
            print(f"✓ Got summary via response.text")
            print(f"Summary: {summary}")
        
        # Method 2: Try via candidates and content
        elif hasattr(response, 'candidates') and response.candidates:
            print(f"Response has {len(response.candidates)} candidate(s)")
            for idx, candidate in enumerate(response.candidates):
                print(f"  Candidate {idx}: {type(candidate).__name__}")
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            summary = part.text.strip()
                            print(f"✓ Got summary via candidates")
                            print(f"Summary: {summary}")
                            break
                if summary:
                    break
        
        # Method 3: Try via parts
        elif hasattr(response, 'parts') and response.parts:
            print(f"Response has {len(response.parts)} part(s)")
            for part in response.parts:
                print(f"  Part type: {type(part).__name__}")
                if hasattr(part, 'text') and part.text:
                    summary = part.text.strip()
                    print(f"✓ Got summary via parts")
                    print(f"Summary: {summary}")
                    break
        
        if not summary:
            print(f"⚠ Warning: No summary was extracted from response")
            print(f"Response object details: {response}")
        
        print(f"{'='*50}")
        print(f"Result: {'Generated' if summary else 'Failed'}")
        print(f"{'='*50}\n")
        
        return summary

    except Exception as e:
        print(f"\n{'='*50}")
        print(f"ERROR in get_ai_summary: {type(e).__name__}: {str(e)}")
        print(f"Generating local fallback summary instead...")
        print(f"{'='*50}\n")
        return generate_local_fallback_summary(text_content)

def generate_local_fallback_summary(text_content):
    """Fallback text summarization that runs locally when the API is disabled or fails."""
    keywords = ["python", "flask", "api", "react", "html", "css", "database", "sql", "git", "web", "deployment"]
    words = text_content.lower().split()
    found_keywords = [word for word in words if any(kw in word for kw in keywords)]
    
    unique_keywords = list(set([kw.strip('.,;:') for kw in found_keywords]))
    word_count = len(words)
    
    if unique_keywords:
        return f"[Local Fallback] The user learned about {', '.join(unique_keywords)} in a structured {word_count}-word entry."
    else:
        return f"[Local Fallback] Documented general programming or non-technical entry containing {word_count} words."
