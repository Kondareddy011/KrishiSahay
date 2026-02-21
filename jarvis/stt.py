import speech_recognition as sr

def listen():
    """
    Listens to the microphone and returns the recognized text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Jarvis] Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("[Jarvis] Processing...")
            query = recognizer.recognize_google(audio)
            print(f"[Farmer] {query}")
            return query
        except sr.WaitTimeoutError:
            print("[Jarvis] I didn't hear anything.")
            return None
        except sr.UnknownValueError:
            print("[Jarvis] I couldn't understand that.")
            return None
        except sr.RequestError as e:
            print(f"[Jarvis] Could not request results; {e}")
            return None
        except Exception as e:
            print(f"[Jarvis] Error: {e}")
            return None

if __name__ == "__main__":
    q = listen()
    if q:
        print(f"Recognized: {q}")
