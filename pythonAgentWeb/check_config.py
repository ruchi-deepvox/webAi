"""Check if all required API keys are configured."""
import os
from dotenv import load_dotenv

load_dotenv(".env.local")

def check_api_keys():
    """Verify all required API keys are present."""
    required_keys = {
        "OPENAI_API_KEY": "OpenAI (LLM - GPT-4.1-mini)",
        "ASSEMBLYAI_API_KEY": "AssemblyAI (Speech-to-Text)",
        "ELEVENLABS_API_KEY": "ElevenLabs (Text-to-Speech)",
        "LIVEKIT_URL": "LiveKit Server URL",
        "LIVEKIT_API_KEY": "LiveKit API Key",
        "LIVEKIT_API_SECRET": "LiveKit API Secret",
    }
    
    optional_keys = {
        "DEEPGRAM_API_KEY": "Deepgram (Alternative STT provider)",
    }
    
    print("=" * 60)
    print("API Configuration Check")
    print("=" * 60)
    
    all_configured = True
    
    print("\n[REQUIRED KEYS]")
    for key, description in required_keys.items():
        value = os.getenv(key)
        if value:
            # Mask the key for security
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"  [OK] {key}: {masked}")
            print(f"       ({description})")
        else:
            print(f"  [MISSING] {key}")
            print(f"            ({description})")
            all_configured = False
    
    print("\n[OPTIONAL KEYS]")
    for key, description in optional_keys.items():
        value = os.getenv(key)
        if value:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"  [OK] {key}: {masked}")
            print(f"       ({description})")
        else:
            print(f"  [NOT SET] {key}")
            print(f"            ({description})")
    
    print("\n" + "=" * 60)
    
    if all_configured:
        print("[SUCCESS] All required API keys are configured!")
        print("\nYou can now run your agent with:")
        print("  uv run python src/agent.py dev")
        return True
    else:
        print("[WARNING] Some required keys are missing.")
        print("\nPlease add them to your .env.local file.")
        return False

if __name__ == "__main__":
    check_api_keys()

