"""
Test script for the Gemini client.
Run this to verify if Gemini is correctly configured.
"""
import sys
import os

# Add parent directory to path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import gemini_client

def test_gemini():
    print("Checking Gemini availability...")
    if not gemini_client.is_available():
        print("FAIL: Gemini not available. Check GEMINI_API_KEY in .env")
        return

    print(f"SUCCESS: Gemini client initialized with model: {gemini_client.GEMINI_MODEL}")
    
    print("\nTesting generation (this will fail if API key is invalid or empty)...")
    prompt = "Give a one-sentence tip for rice farmers."
    resp = gemini_client.generate(prompt=prompt)
    
    if resp:
        print(f"Response: {resp}")
        print("SUCCESS: Generation works!")
    else:
        print("FAIL: Generation returned None. Check API key validity or credit.")

if __name__ == "__main__":
    test_gemini()
