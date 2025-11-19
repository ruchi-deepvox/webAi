"""Test if TTS (Cartesia) is working properly."""
import asyncio
import os
from dotenv import load_dotenv
from livekit.agents import inference

load_dotenv(".env.local")

async def test_tts():
    """Test Cartesia TTS."""
    print("=" * 60)
    print("Testing Cartesia TTS")
    print("=" * 60)
    
    cartesia_key = os.getenv("CARTESIA_API_KEY")
    if not cartesia_key:
        print("[ERROR] CARTESIA_API_KEY not found in .env.local")
        return False
    
    print(f"[OK] Cartesia API Key: {cartesia_key[:10]}...")
    
    try:
        print("\n[INFO] Creating TTS instance...")
        tts = inference.TTS(
            model="cartesia/sonic-3",
            voice="9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
        )
        
        print("[INFO] Initializing TTS...")
        await tts.__aenter__()
        
        print("[INFO] Generating test audio...")
        test_text = "Hello! This is a test of the text to speech system."
        
        async for chunk in tts.synthesize(text=test_text):
            print(f"[OK] Generated audio chunk: {len(chunk.data.frame.data)} bytes")
        
        await tts.__aexit__(None, None, None)
        
        print("\n" + "=" * 60)
        print("[SUCCESS] Cartesia TTS is working correctly!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] TTS test failed: {e}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    asyncio.run(test_tts())

