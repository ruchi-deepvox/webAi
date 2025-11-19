# ⚡ Quick Reference - Custom Agent Prompt via API

## 🎯 The Simple Way

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a pirate. Speak like a pirate!"
  }'
```

## 💻 In Your Code

```javascript
const { token, url } = await fetch('http://localhost:8000/api/connect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        instructions: "Your custom prompt here",
        tts_provider: "cartesia",  // or "elevenlabs"
        voice_id: "optional-voice-id"  // leave empty for default
    })
}).then(r => r.json());
```

## 🎭 Ready-to-Use Prompts

### Pirate Captain 🏴‍☠️
```
"You are a pirate captain. Always speak like a pirate with 'Ahoy!' and 'Arr matey!'"
```

### Fitness Coach 💪
```
"You are an energetic fitness coach. Motivate users and provide workout tips enthusiastically!"
```

### Professional Support 🎧
```
"You are a professional customer support agent. Be polite, patient, and always confirm understanding before providing solutions."
```

### Friendly Chef 👨‍🍳
```
"You are a friendly chef. Share cooking tips and recipes. Make everything sound delicious!"
```

## ✅ What You Need Running

```bash
# Terminal 1
uv run python unified_api.py

# Terminal 2  
uv run python src/agent.py dev
```

## 📁 Files Created

- **`CUSTOM_PROMPT_GUIDE.md`** - Complete guide with examples
- **`custom_prompt_example.html`** - Working demo (OPEN NOW!)
- **`TTS_VOICE_GUIDE.md`** - TTS provider & voice selection guide
- **`portable_voice_ui.html`** - Full UI with TTS selection

## 🎵 TTS Voice Options

### Use Cartesia (Default - Fast)
```json
{
  "tts_provider": "cartesia",
  "voice_id": "9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"
}
```

### Use ElevenLabs (High Quality)
```json
{
  "tts_provider": "elevenlabs",
  "voice_id": "0p0kYzKW1Gq5uoKh8Qod"
}
```

📖 **See `TTS_VOICE_GUIDE.md` for all available voices!**

## 🚀 Try It!

1. Open `custom_prompt_example.html` (just opened!)
2. Click a template button OR write your own
3. Click "Connect with Custom Prompt"
4. Talk to your customized agent!

**That's it!** 🎉

