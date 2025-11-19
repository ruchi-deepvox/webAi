# 🎤 TTS Voice Configuration Guide

Switch between **Cartesia** and **ElevenLabs** TTS providers with custom voice IDs!

---

## 📋 Quick Reference

### API Parameters

Add these to your `/api/connect` request:

```json
{
  "tts_provider": "cartesia",     // or "elevenlabs"
  "voice_id": "your-voice-id",    // optional
  "instructions": "Your prompt",   // optional
  "room_name": "my-room",         // optional
  "user_name": "John Doe"         // optional
}
```

---

## 🎵 Available TTS Providers

### 1. **Cartesia** (Default - Fast & Natural)
- **Provider ID:** `cartesia`
- **Model:** `sonic-3`
- **Default Voice:** `9626c31c-bec5-4cca-baa8-f8ba9e84c8bc`
- **Speed:** ⚡ Very Fast
- **Quality:** 🌟🌟🌟🌟
- **Cost:** 💰 Lower

**Popular Cartesia Voices:**
- `9626c31c-bec5-4cca-baa8-f8ba9e84c8bc` - Natural & Clear (Default)
- `79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e` - British Male
- `a167e0f3-df7e-4d52-a9c3-f949145efdab` - American Female
- `b7d50908-b17c-442d-ad8d-810c63997ed9` - British Female

[Browse all Cartesia voices →](https://docs.cartesia.ai/get-started/available-voices)

---

### 2. **ElevenLabs** (High Quality & Expressive)
- **Provider ID:** `elevenlabs`
- **Model:** `eleven_turbo_v2_5`
- **Default Voice:** `0p0kYzKW1Gq5uoKh8Qod`
- **Speed:** ⚡ Fast
- **Quality:** 🌟🌟🌟🌟🌟
- **Cost:** 💰💰 Higher

**Popular ElevenLabs Voices:**
- `0p0kYzKW1Gq5uoKh8Qod` - Natural & Warm (Default)
- `21m00Tcm4TlvDq8ikWAM` - Rachel - Calm & Professional
- `EXAVITQu4vr4xnSDxMaL` - Sarah - Soft & Friendly
- `pNInz6obpgDQGcFmaJgB` - Adam - Deep & Authoritative

[Browse all ElevenLabs voices →](https://elevenlabs.io/voice-library)

---

## 🚀 Usage Examples

### Example 1: Default Cartesia (Fastest)

```bash
curl -X POST http://192.168.0.102:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "instructions": "You are a helpful assistant"
  }'
```

**Result:** Uses Cartesia with default voice ✅

---

### Example 2: ElevenLabs with Default Voice

```bash
curl -X POST http://192.168.0.102:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "tts_provider": "elevenlabs",
    "instructions": "You are a professional consultant"
  }'
```

**Result:** Uses ElevenLabs `0p0kYzKW1Gq5uoKh8Qod` ✅

---

### Example 3: ElevenLabs with Custom Voice

```bash
curl -X POST http://192.168.0.102:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "tts_provider": "elevenlabs",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "instructions": "You are Rachel, a professional assistant"
  }'
```

**Result:** Uses ElevenLabs with Rachel's voice ✅

---

### Example 4: Cartesia with Custom Voice

```bash
curl -X POST http://192.168.0.102:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "tts_provider": "cartesia",
    "voice_id": "79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e",
    "instructions": "You are a British gentleman assistant"
  }'
```

**Result:** Uses Cartesia British Male voice ✅

---

## 🎨 Using the UI

The **`portable_voice_ui.html`** includes TTS selection!

### Steps:
1. **Open** `portable_voice_ui.html`
2. **Select TTS Provider:**
   - Cartesia (Fast & Natural) - Default
   - ElevenLabs (High Quality)
3. **Enter Voice ID** (optional):
   - Leave empty for default voice
   - Hint shows the default voice ID for each provider
4. **Enter Instructions** (optional)
5. **Click "Connect & Talk"**

---

## 🔑 API Keys Required

Make sure these are set in `.env.local`:

### For Cartesia:
```bash
CARTESIA_API_KEY=sk_car_xxxxx
```

### For ElevenLabs:
```bash
ELEVENLABS_API_KEY=sk_xxxxx
```

### Always Required:
```bash
OPENAI_API_KEY=sk-proj-xxxxx
ASSEMBLYAI_API_KEY=xxxxx
LIVEKIT_URL=wss://your-livekit-url
LIVEKIT_API_KEY=xxxxx
LIVEKIT_API_SECRET=xxxxx
```

---

## 💡 Choosing the Right Provider

### Use **Cartesia** when:
- ✅ Speed is critical
- ✅ Lower cost is important
- ✅ Natural voice is sufficient
- ✅ Building conversational AI

### Use **ElevenLabs** when:
- ✅ Voice quality is paramount
- ✅ Need maximum expressiveness
- ✅ Creating content or podcasts
- ✅ Budget allows for premium quality

---

## 🧪 Testing Different Voices

### Test Script:

```python
import requests

voices_to_test = [
    {"provider": "cartesia", "voice_id": None, "name": "Cartesia Default"},
    {"provider": "elevenlabs", "voice_id": None, "name": "ElevenLabs Default"},
    {"provider": "elevenlabs", "voice_id": "21m00Tcm4TlvDq8ikWAM", "name": "Rachel"},
]

for voice in voices_to_test:
    print(f"Testing: {voice['name']}")
    
    payload = {
        "user_name": "Tester",
        "tts_provider": voice['provider'],
        "instructions": f"Say: Testing {voice['name']}"
    }
    
    if voice['voice_id']:
        payload['voice_id'] = voice['voice_id']
    
    response = requests.post(
        'http://192.168.0.102:8000/api/connect',
        json=payload
    )
    
    print(f"Result: {response.json()}\n")
```

---

## 📊 Voice Comparison

| Feature | Cartesia | ElevenLabs |
|---------|----------|------------|
| **Speed** | ⚡⚡⚡ Very Fast | ⚡⚡ Fast |
| **Quality** | 🌟🌟🌟🌟 Great | 🌟🌟🌟🌟🌟 Excellent |
| **Expressiveness** | Good | Excellent |
| **Languages** | 30+ | 30+ |
| **Cost** | $ Lower | $$ Higher |
| **Best For** | Real-time chat | Content creation |

---

## 🔧 Troubleshooting

### Voice Not Working?

1. **Check API Keys:**
   ```bash
   # For Cartesia
   echo $CARTESIA_API_KEY
   
   # For ElevenLabs
   echo $ELEVENLABS_API_KEY
   ```

2. **Verify Voice ID:**
   - Make sure voice ID is correct
   - Try with default voice (leave empty)

3. **Check Logs:**
   ```bash
   # In the terminal running the agent
   # Look for: "Configured [Provider] TTS with voice: [ID]"
   ```

4. **Test Provider:**
   ```bash
   curl http://192.168.0.102:8000/api/health
   ```

### Agent Not Using Selected Voice?

- Make sure agent is restarted after changing API keys
- Check metadata is being passed correctly
- Look at agent logs for TTS configuration

---

## 🎯 Pro Tips

1. **Mix and Match:**
   - Use Cartesia for speed
   - Switch to ElevenLabs for important interactions

2. **Voice Consistency:**
   - Keep same voice throughout conversation
   - Don't switch mid-session

3. **Test Before Production:**
   - Try different voices
   - Check latency on your network
   - Verify API costs

4. **Optimize for Use Case:**
   - **Customer Service:** Cartesia (speed)
   - **Storytelling:** ElevenLabs (quality)
   - **Virtual Assistant:** Cartesia (efficiency)
   - **Podcasts:** ElevenLabs (expressiveness)

---

## 📚 Additional Resources

- [Cartesia Documentation](https://docs.cartesia.ai/)
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library)
- [LiveKit TTS Docs](https://docs.livekit.io/agents/models/tts/)

---

## ✨ Summary

**New API Parameters:**
- `tts_provider`: `"cartesia"` or `"elevenlabs"`
- `voice_id`: Custom voice ID (optional)

**Defaults:**
- Provider: Cartesia
- Cartesia Voice: `9626c31c-bec5-4cca-baa8-f8ba9e84c8bc`
- ElevenLabs Voice: `0p0kYzKW1Gq5uoKh8Qod`

**Use the UI or API - Your choice!** 🎉

