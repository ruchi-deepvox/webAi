# 🎯 Custom Agent Prompt/Instructions via API

You can now change the agent's personality, behavior, and instructions dynamically via the API!

---

## 🚀 How It Works

Simply pass `instructions` parameter when connecting to the API:

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a pirate captain. Speak like a pirate!"
  }'
```

---

## 📝 Examples

### Example 1: Pirate Agent

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "User",
    "room_name": "pirate-room",
    "instructions": "You are a pirate captain named Captain Blackbeard. Always speak like a pirate with phrases like Ahoy, Arr, and matey. Be enthusiastic and adventurous."
  }'
```

### Example 2: Customer Support Agent

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a professional customer support agent for TechCorp. Be polite, patient, and helpful. Always confirm you understand the customer's issue before providing solutions."
  }'
```

### Example 3: Fitness Coach

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type": application/json" \
  -d '{
    "instructions": "You are an energetic fitness coach. Motivate users with enthusiasm. Provide workout tips and healthy lifestyle advice. Always be encouraging and positive."
  }'
```

### Example 4: Language Tutor

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a Spanish language tutor. Help users learn Spanish by speaking slowly and clearly. Correct their mistakes gently and provide encouragement. Mix English and simple Spanish phrases."
  }'
```

---

## 💻 Using in Your UI

### Vanilla JavaScript

```html
<script type="module">
import { Room } from 'https://cdn.jsdelivr.net/npm/livekit-client/dist/livekit-client.esm.mjs';

// Custom instructions
const customPrompt = "You are a friendly chef. Give cooking tips and recipes.";

// Connect with custom prompt
const { token, url } = await fetch('http://localhost:8000/api/connect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        room_name: `room-${Date.now()}`,
        instructions: customPrompt  // ← Custom prompt here!
    })
}).then(r => r.json());

// Connect to agent
const room = new Room();
await room.connect(url, token);
await room.localParticipant.setMicrophoneEnabled(true);
</script>
```

---

### React Example

```jsx
import { Room } from 'livekit-client';
import { useState } from 'react';

function CustomAgent() {
    const [prompt, setPrompt] = useState('');

    const connect = async () => {
        const { token, url } = await fetch('http://localhost:8000/api/connect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                room_name: `room-${Date.now()}`,
                instructions: prompt  // Use custom prompt
            })
        }).then(r => r.json());

        const room = new Room();
        await room.connect(url, token);
        await room.localParticipant.setMicrophoneEnabled(true);
    };

    return (
        <div>
            <textarea
                placeholder="Enter custom instructions..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
            />
            <button onClick={connect}>Connect with Custom Prompt</button>
        </div>
    );
}
```

---

### Vue.js Example

```vue
<template>
    <div>
        <textarea
            v-model="customPrompt"
            placeholder="Enter custom instructions..."
        />
        <button @click="connect">Connect with Custom Prompt</button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { Room } from 'livekit-client';

const customPrompt = ref('');

const connect = async () => {
    const { token, url } = await fetch('http://localhost:8000/api/connect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            room_name: `room-${Date.now()}`,
            instructions: customPrompt.value
        })
    }).then(r => r.json());

    const room = new Room();
    await room.connect(url, token);
    await room.localParticipant.setMicrophoneEnabled(true);
};
</script>
```

---

## 🎨 Prompt Templates

### Professional Business Agent
```
You are a professional business assistant. Maintain a formal tone, be concise, and focus on providing actionable business insights. Always confirm important details before proceeding.
```

### Friendly Casual Agent
```
You are a friendly and casual AI assistant. Use a warm, conversational tone. Be approachable and relatable. Use simple language and occasional humor to make conversations enjoyable.
```

### Technical Support Agent
```
You are a technical support specialist. Be patient and thorough when explaining technical concepts. Break down complex issues into simple steps. Always ask clarifying questions before suggesting solutions.
```

### Sales Assistant
```
You are a sales assistant. Be enthusiastic about products but not pushy. Listen to customer needs, ask qualifying questions, and provide personalized recommendations. Build rapport naturally.
```

### Medical Receptionist
```
You are a medical office receptionist. Be professional, empathetic, and HIPAA-compliant. Never provide medical advice. Help with appointments, general questions, and direct urgent matters appropriately.
```

---

## 🔧 API Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `instructions` | string | No | Custom prompt/personality for the agent |
| `room_name` | string | No | Custom room name |
| `user_id` | string | No | User identifier |
| `user_name` | string | No | User display name |

---

## 📊 API Response

When you include `instructions`, they're returned in the response:

```json
{
    "success": true,
    "token": "eyJh...",
    "url": "wss://...",
    "room": "room-123",
    "identity": "user-123",
    "name": "User",
    "instructions": "Your custom prompt here"
}
```

---

## ⚡ Quick Start

1. **Start your backend:**
   ```bash
   # Terminal 1
   uv run python unified_api.py
   
   # Terminal 2
   uv run python src/agent.py dev
   ```

2. **Test with curl:**
   ```bash
   curl -X POST http://localhost:8000/api/connect \
     -H "Content-Type: application/json" \
     -d '{"instructions": "You are a helpful assistant."}'
   ```

3. **Use in your UI:**
   ```javascript
   fetch('http://localhost:8000/api/connect', {
       method: 'POST',
       body: JSON.stringify({
           instructions: "Your custom prompt here"
       })
   })
   ```

---

## 💡 Best Practices

### 1. Be Specific
```
❌ Bad: "Be helpful"
✅ Good: "You are a customer service agent. Always greet users warmly, listen actively, and provide clear solutions."
```

### 2. Define Boundaries
```
✅ "You are a legal assistant. Provide general information only. Always remind users to consult with a licensed attorney for legal advice."
```

### 3. Set Tone and Style
```
✅ "You are an energetic radio DJ. Be upbeat, use current slang, and keep responses short and punchy."
```

### 4. Include Response Format
```
✅ "Keep all responses under 3 sentences. Use simple language. Avoid technical jargon."
```

---

## 🐛 Troubleshooting

### Instructions Not Working?

1. **Check logs:**
   Look for: `Agent initialized with custom instructions` in agent terminal

2. **Restart agent:**
   Stop and restart `uv run python src/agent.py dev`

3. **Test with simple prompt:**
   ```bash
   curl -X POST http://localhost:8000/api/connect \
     -d '{"instructions": "Always say hello first"}'
   ```

### Default Behavior?

If no `instructions` provided, agent uses default:
```
"You are a helpful voice AI assistant. You eagerly assist users with their questions..."
```

---

## 🎯 Use Cases

- **Multi-tenant apps** - Different personalities per customer
- **A/B testing** - Test different agent personalities
- **Contextual agents** - Change behavior based on user type
- **Dynamic branding** - Match agent to your brand voice
- **Specialized workflows** - Sales, support, education, etc.

---

## 📚 More Examples

Check these files:
- `minimal_example.html` - Basic implementation
- `READY_TO_USE_CODE.md` - Code for all frameworks
- `API_DOCUMENTATION.md` - Full API reference

---

**You now have complete control over your agent's personality via API!** 🎉

