import os
import sys

# Add backend to path to reuse gemini_client
try:
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file_path))
    backend_path = os.path.join(project_root, "backend")
    
    if backend_path not in sys.path:
        sys.path.append(backend_path)
    
    import gemini_client
except Exception as e:
    print(f"[Jarvis] Warning: Could not load gemini_client from {backend_path if 'backend_path' in locals() else 'unknown'}")
    print(f"[Jarvis] Error detail: {e}")
    gemini_client = None

def get_ai_response(query):
    """
    Gets a response from Gemini AI for the voice assistant.
    """
    if not gemini_client or not gemini_client.is_available():
        return "I'm sorry, my AI brain is not connected right now. Please check your API key."
        
    system_prompt = (
        "You are Jarvis, a helpful and friendly agricultural voice assistant for Indian farmers. "
        "Keep your responses concise, human-like, and easy to understand when spoken. "
        "Provide actionable agricultural advice."
    )
    
    response = gemini_client.generate(prompt=query, system_prompt=system_prompt, max_tokens=256)
    
    if not response:
        return "I encountered an error while thinking. Can you repeat that?"
        
    return response

if __name__ == "__main__":
    test_query = "What are the best crops for monsoon season?"
    print(f"Query: {test_query}")
    print(f"Response: {get_ai_response(test_query)}")
