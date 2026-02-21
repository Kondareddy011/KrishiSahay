"""
Offline-capable generative AI via Ollama (local LLM).
Run: ollama run llama3.2  (or mistral, gemma2, etc.)
"""

import os
import json
import urllib.request
import urllib.error
from typing import Optional

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "60"))


def _ollama_available() -> bool:
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False


def generate(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 512,
) -> Optional[str]:
    """
    Generate response using Ollama. Returns None if Ollama is unavailable.
    """
    try:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        body = {
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(
            f"{OLLAMA_URL}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
            out = json.loads(resp.read().decode("utf-8"))
        return out.get("response", "").strip() or None
    except Exception as e:
        print(f"Ollama generate error: {e}")
        return None


def is_available() -> bool:
    return _ollama_available()
