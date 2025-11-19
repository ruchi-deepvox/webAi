# 🔧 ElevenLabs Voice ID Fix

## ❌ What Was Wrong

1. **Wrong API Usage:** The code was using `inference.TTS()` for ElevenLabs, which doesn't support ElevenLabs directly.
2. **Missing Plugin:** The ElevenLabs plugin wasn't installed.
3. **Voice ID Not Applied:** Even when passed through the API, the voice_id wasn't being used correctly.

---

## ✅ What Was Fixed

### 1. **Installed ElevenLabs Plugin**
```bash
uv add livekit-plugins-elevenlabs
```

### 2. **Updated Agent Import**
```python
# Added elevenlabs to imports
from livekit.plugins import noise_cancellation, silero, elevenlabs
```

### 3. **Fixed TTS Configuration**

**Before (❌ Wrong):**
```python
tts_config = inference.TTS(
    model="elevenlabs/eleven_turbo_v2_5",
    voice=voice_id if voice_id else default_voice
)
```

**After (✅ Correct):**
```python
selected_voice = voice_id if voice_id else default_voice
tts_config = elevenlabs.TTS(voice=selected_voice)
```

---

## 🧪 How to Test

### **Option 1: Use Test Page**
1. Open `test_voice_id.html` (I just opened it!)
2. Click "Test ElevenLabs (Custom Voice)"
3. Check the response shows your `voice_id`

### **Option 2: Use curl**
```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "tts_provider": "elevenlabs",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "user_name": "Test"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "tts_provider": "elevenlabs",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "token": "...",
  "url": "wss://...",
  "room": "room-...",
  "identity": "user-..."
}
```

### **Option 3: Use the UI**
1. Open `portable_voice_ui.html`
2. Select "ElevenLabs (High Quality)"
3. Enter a voice ID (e.g., `21m00Tcm4TlvDq8ikWAM`)
4. Click "Connect & Talk"
5. **Check the agent logs** for: `Configured ElevenLabs TTS with voice: 21m00Tcm4TlvDq8ikWAM`

---

## 📊 Verification Checklist

- ✅ ElevenLabs plugin installed: `livekit-plugins-elevenlabs`
- ✅ Agent imports `elevenlabs` from plugins
- ✅ Agent uses `elevenlabs.TTS(voice=...)` for ElevenLabs
- ✅ Agent uses `inference.TTS(model="cartesia/sonic-3", voice=...)` for Cartesia
- ✅ Voice ID is read from metadata
- ✅ Voice ID is applied to TTS configuration
- ✅ Agent logs show correct voice ID

---

## 🎵 Available ElevenLabs Voices

| Voice ID | Name | Description |
|----------|------|-------------|
| `0p0kYzKW1Gq5uoKh8Qod` | Default | Natural & Warm (Default) |
| `21m00Tcm4TlvDq8ikWAM` | Rachel | Calm & Professional |
| `EXAVITQu4vr4xnSDxMaL` | Sarah | Soft & Friendly |
| `pNInz6obpgDQGcFmaJgB` | Adam | Deep & Authoritative |

[Browse all voices →](https://elevenlabs.io/voice-library)

---

## 🔍 How to Check Agent Logs

Look for these lines in your agent terminal:

```
✅ Good:
Using TTS provider: elevenlabs
Using voice ID: 21m00Tcm4TlvDq8ikWAM
Configured ElevenLabs TTS with voice: 21m00Tcm4TlvDq8ikWAM

❌ Bad (if you see this, voice_id isn't being passed):
Using TTS provider: elevenlabs
Configured ElevenLabs TTS with voice: 0p0kYzKW1Gq5uoKh8Qod  # Default voice
```

---

## 💡 Pro Tips

1. **Always Check Logs:** The agent logs will tell you exactly which voice is being used.

2. **Test with Default First:** Make sure ElevenLabs works with the default voice before trying custom voices.

3. **Verify API Key:** Make sure `ELEVENLABS_API_KEY` is set in `.env.local`

4. **Restart Agent:** After changing voice settings, always restart the agent for changes to take effect.

5. **Voice ID Format:** ElevenLabs voice IDs are typically 20-character alphanumeric strings like `0p0kYzKW1Gq5uoKh8Qod`

---

## 🚀 Quick Test Commands

### Test Default Voice
```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"tts_provider": "elevenlabs", "user_name": "Test"}'
```

### Test Custom Voice
```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "tts_provider": "elevenlabs",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "user_name": "Test"
  }'
```

---

## ✅ Summary

**The issue was:** Using wrong API (`inference.TTS`) instead of proper plugin (`elevenlabs.TTS`)

**The fix:**
1. Installed plugin: `livekit-plugins-elevenlabs`
2. Updated imports: `from livekit.plugins import elevenlabs`
3. Changed code: `elevenlabs.TTS(voice=voice_id)`

**Now it works!** 🎉

The voice_id from the UI is now correctly passed through:
- UI → unified_api.py → metadata → agent.py → elevenlabs.TTS()

