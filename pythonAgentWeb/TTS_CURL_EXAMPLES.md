# 🎤 TTS Voice Selection - curl Examples

Quick copy-paste curl commands to test different TTS providers and voices!

---

## 🚀 Basic Examples

### 1. Default (Cartesia with default voice)

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "instructions": "You are a helpful assistant"
  }'
```

---

### 2. ElevenLabs (Default Voice)

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "tts_provider": "elevenlabs",
    "instructions": "You are a professional assistant"
  }'
```

**Voice Used:** `0p0kYzKW1Gq5uoKh8Qod` (ElevenLabs default)

---

### 3. ElevenLabs (Rachel - Professional)

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "tts_provider": "elevenlabs",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "instructions": "You are Rachel, a professional consultant"
  }'
```

---

### 4. Cartesia (British Male)

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "tts_provider": "cartesia",
    "voice_id": "79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e",
    "instructions": "You are a British gentleman assistant"
  }'
```

---

## 🎭 Use Case Examples

### Customer Service (ElevenLabs - Rachel)

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Customer",
    "tts_provider": "elevenlabs",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "instructions": "You are a professional customer service representative. Be polite, patient, and helpful. Always confirm understanding before providing solutions."
  }'
```

---

### Fitness Coach (Cartesia - Energetic)

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Athlete",
    "tts_provider": "cartesia",
    "instructions": "You are an energetic fitness coach! Motivate users with enthusiasm and provide workout tips!"
  }'
```

---

### Storyteller (ElevenLabs - Deep Voice)

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Listener",
    "tts_provider": "elevenlabs",
    "voice_id": "pNInz6obpgDQGcFmaJgB",
    "instructions": "You are a captivating storyteller. Use dramatic pauses and vivid descriptions."
  }'
```

---

### Meditation Guide (ElevenLabs - Soft & Calm)

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "User",
    "tts_provider": "elevenlabs",
    "voice_id": "EXAVITQu4vr4xnSDxMaL",
    "instructions": "You are a calm meditation guide. Speak slowly and soothingly. Guide users through relaxation exercises."
  }'
```

---

## 🌐 From Other Devices

Replace `localhost` with your server IP:

```bash
curl -X POST http://192.168.0.102:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John",
    "tts_provider": "elevenlabs",
    "voice_id": "21m00Tcm4TlvDq8ikWAM",
    "instructions": "Your custom prompt"
  }'
```

---

## 🎵 Available Voice IDs

### Cartesia
- `9626c31c-bec5-4cca-baa8-f8ba9e84c8bc` - Natural & Clear (Default)
- `79f8b5fb-2cc8-479a-80df-29f7a7cf1a3e` - British Male
- `a167e0f3-df7e-4d52-a9c3-f949145efdab` - American Female
- `b7d50908-b17c-442d-ad8d-810c63997ed9` - British Female

### ElevenLabs
- `0p0kYzKW1Gq5uoKh8Qod` - Natural & Warm (Default)
- `21m00Tcm4TlvDq8ikWAM` - Rachel (Professional)
- `EXAVITQu4vr4xnSDxMaL` - Sarah (Soft)
- `pNInz6obpgDQGcFmaJgB` - Adam (Deep)

---

## ✅ Test Response

Successful response:

```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "url": "wss://voice-xxx.livekit.cloud",
  "room": "room-1234567890",
  "identity": "user-1234567890",
  "name": "John",
  "tts_provider": "elevenlabs",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "instructions": "Your custom prompt"
}
```

---

## 🔧 PowerShell (Windows)

```powershell
$body = @{
    user_name = "John"
    tts_provider = "elevenlabs"
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    instructions = "You are a helpful assistant"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/connect" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

---

## 🐍 Python

```python
import requests

response = requests.post(
    'http://localhost:8000/api/connect',
    json={
        'user_name': 'John',
        'tts_provider': 'elevenlabs',
        'voice_id': '21m00Tcm4TlvDq8ikWAM',
        'instructions': 'You are a helpful assistant'
    }
)

data = response.json()
print(f"Token: {data['token']}")
print(f"TTS: {data['tts_provider']}")
print(f"Voice: {data.get('voice_id', 'default')}")
```

---

## 🧪 Test All Providers

```bash
#!/bin/bash

echo "Testing Cartesia..."
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"tts_provider": "cartesia", "user_name": "Test"}'

echo "\n\nTesting ElevenLabs..."
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"tts_provider": "elevenlabs", "user_name": "Test"}'
```

---

## 💡 Pro Tips

1. **Test with default first:**
   - Don't specify `voice_id`
   - Verify provider works

2. **Check API keys:**
   ```bash
   curl http://localhost:8000/api/health
   ```

3. **Monitor agent logs:**
   - Look for: "Configured [Provider] TTS with voice: [ID]"

4. **Compare quality:**
   - Test same prompt with both providers
   - Choose based on your needs

---

## 📚 More Info

- **Full Guide:** `TTS_VOICE_GUIDE.md`
- **Quick Reference:** `QUICK_CUSTOM_PROMPT.md`
- **UI Example:** `portable_voice_ui.html`

---

**Copy, paste, and customize!** 🎉

