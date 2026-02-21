import pyttsx3

def speak(text):
    """
    Converts text to speech and plays it.
    """
    engine = pyttsx3.init()
    
    # Configure voice
    voices = engine.getProperty('voices')
    # Try to find a male/natural voice
    for voice in voices:
        if "male" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
            
    engine.setProperty('rate', 170) # Speed of speech
    engine.setProperty('volume', 0.9) # Volume (0.0 to 1.0)
    
    print(f"[Jarvis] {text}")
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Hello, I am Jarvis. How can I help you today?")
