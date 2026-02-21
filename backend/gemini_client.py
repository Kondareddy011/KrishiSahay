"""
Generative AI via Google Gemini API (new google-genai SDK).
Requires GEMINI_API_KEY in .env file.
"""

import os
from typing import Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# Initialize client
client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")

def generate(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 512,
) -> Optional[str]:
    """
    Generate response using Gemini. Returns None if client not configured or API error.
    """
    if not client:
        return None
        
    try:
        # Try primary model
        model_names = [GEMINI_MODEL, "gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest"]
        last_err = None
        
        for m_name in model_names:
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt if system_prompt else None,
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    )
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                last_err = e
                # Don't flood logs with intermediate fallback errors unless all fail
                continue
        
        if last_err:
            print(f"Gemini all models failed. Last error: {last_err}")
        return None
    except Exception as e:
        print(f"Gemini generate unexpected error: {e}")
        return None

def analyze_image(
    image_data: bytes,
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 1024,
) -> Optional[str]:
    """
    Analyze an image using Gemini's multimodal capabilities.
    """
    if not client:
        return None
        
    try:
        model_names = [GEMINI_MODEL, "gemini-2.0-flash", "gemini-1.5-flash", "gemini-flash-latest"]
        last_err = None
        
        # Create image part
        image_part = types.Part.from_bytes(
            data=image_data,
            mime_type="image/jpeg" # PIL usually handles conversion to RGB/JPEG format if needed
        )
        
        for m_name in model_names:
            try:
                response = client.models.generate_content(
                    model=m_name,
                    contents=[image_part, prompt],
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt if system_prompt else None,
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    )
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                last_err = e
                continue
        
        if last_err:
            print(f"Gemini Vision all models failed. Last error: {last_err}")
        return None
    except Exception as e:
        print(f"Gemini Vision unexpected error: {e}")
        return None

def is_available() -> bool:
    """Check if Gemini is configured."""
    return client is not None and GEMINI_API_KEY is not None and GEMINI_API_KEY.strip() != ""
