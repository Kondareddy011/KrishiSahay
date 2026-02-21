import os
import sys
import subprocess
import traceback

def main():
    # Ensure we are in the project root
    current_script_path = os.path.abspath(__file__)
    # If this is in project/ , the root is current dir. 
    # If this is in project/jarvis/, the root is one level up.
    potential_root = os.path.dirname(current_script_path)
    if os.path.basename(potential_root) == "jarvis":
        project_root = os.path.dirname(potential_root)
    else:
        project_root = potential_root
        
    os.chdir(project_root)
    
    print("="*40)
    print("      Jarvis Voice Assistant Launcher      ")
    print("="*40)

    # 1. Check for basic dependencies
    essential_deps = ["pyaudio", "speech_recognition", "pyttsx3", "google.genai", "dotenv"]
    missing_deps = []
    
    for dep in essential_deps:
        try:
            if dep == "google.genai":
                from google import genai
            elif dep == "dotenv":
                import dotenv
            else:
                __import__(dep)
        except ImportError:
            missing_deps.append(dep)
            
    if missing_deps:
        print(f"[*] Missing dependencies: {', '.join(missing_deps)}")
        print("[*] Attempting to install them automatically...")
        try:
            # Map module names to pip package names
            package_map = {
                "speech_recognition": "SpeechRecognition",
                "google.genai": "google-genai",
                "dotenv": "python-dotenv"
            }
            install_list = [package_map.get(d, d) for d in missing_deps]
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + install_list)
            print("[+] Installation successful!")
        except Exception as e:
            print(f"[-] Installation failed: {e}")
            print("Please run: pip install SpeechRecognition pyttsx3 pyaudio google-genai python-dotenv")
            return

    # 2. Check gemini_client manually
    sys.path.append(os.path.join(project_root, "backend"))
    try:
        import gemini_client
        if not gemini_client.is_available():
            print("[!] Warning: Gemini API Key not found in backend/.env")
    except Exception as e:
        print(f"[!] Warning: Could not initialize backend engine: {e}")
        # traceback.print_exc()

    # 3. Launch Jarvis
    print("\n[+] Launching Jarvis...")
    try:
        # Use subprocess to run it to keep environment clean
        subprocess.run([sys.executable, "jarvis/main.py"])
    except KeyboardInterrupt:
        print("\n[+] Jarvis closed.")
    except Exception as e:
        print(f"[-] Fatal error launching Jarvis: {e}")

if __name__ == "__main__":
    main()
