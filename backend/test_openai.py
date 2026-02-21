"""
Test script for the OpenAI client.
Run this to verify if OpenAI is correctly configured.
"""
import sys
import os

# Add parent directory to path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import openai_client

def test_openai():
    print("Checking OpenAI availability...")
    if not openai_client.is_available():
        print("FAIL: OpenAI not available. Check OPENAI_API_KEY in .env")
        return

    print(f"SUCCESS: OpenAI client initialized with model: {openai_client.OPENAI_MODEL}")
    
    print("\nTesting generation (this will fail if API key is invalid or empty)...")
    prompt = "Give a one-sentence tip for rice farmers."
    resp = openai_client.generate(prompt=prompt)
    
    if resp:
        print(f"Response: {resp}")
        print("SUCCESS: Generation works!")
    else:
        print("FAIL: Generation returned None. Check API key validity or credit.")

if __name__ == "__main__":
    test_openai()
