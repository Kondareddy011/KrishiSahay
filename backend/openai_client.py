"""
Generative AI via OpenAI API.
Requires OPENAI_API_KEY in .env file.
"""

import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Initialize client
client = None
if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")

def generate(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 512,
) -> Optional[str]:
    """
    Generate response using OpenAI. Returns None if client not initialized or API error.
    """
    if not client:
        return None
        
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return response.choices[0].message.content.strip() or None
    except Exception as e:
        print(f"OpenAI generate error: {e}")
        return None

def is_available() -> bool:
    """Check if OpenAI is configured and likely available."""
    return client is not None and OPENAI_API_KEY is not None
