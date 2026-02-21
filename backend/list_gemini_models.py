import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found in .env")
    exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

try:
    print("Listing models...")
    for model in client.models.list():
        print(f"Model ID: {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
