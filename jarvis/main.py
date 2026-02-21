import os
import sys

# Add the current directory to sys.path so it can find stt, tts, engine
jarvis_dir = os.path.dirname(os.path.abspath(__file__))
if jarvis_dir not in sys.path:
    sys.path.append(jarvis_dir)

from stt import listen
from tts import speak
from engine import get_ai_response
import time

def main():
    """
    Main loop for the Jarvis voice assistant.
    """
    speak("Hello! I am Jarvis, your agricultural assistant. How can I help you today?")
    
    while True:
        try:
            # Step 1: Listen to Farmer
            user_input = listen()
            
            if user_input:
                # Basic check for exit commands
                if any(word in user_input.lower() for word in ["exit", "stop", "goodbye", "quit"]):
                    speak("Goodbye! Happy farming.")
                    break
                
                # Step 2: Get AI Response
                print("[Jarvis] Thinking...")
                response = get_ai_response(user_input)
                
                # Step 3: Speak Back to Farmer
                speak(response)
            
            # Short pause to prevent overlapping
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            speak("Powering down. Goodbye!")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            speak("I encountered a hiccup. Let's try again.")
            time.sleep(1)

if __name__ == "__main__":
    main()
