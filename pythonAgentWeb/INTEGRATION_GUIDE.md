# 🚀 Integration Guide - Using the API Response

## You Got This Response:

```json
{
    "identity": "user-123",
    "name": "John",
    "room": "my-room",
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "url": "wss://voice-4luxbgpy.livekit.cloud"
}
```

## Here's How to Use It:

---

## 🎯 The 5-Step Integration

### Step 1: Call Your API (You Already Did This! ✅)

```javascript
const response = await fetch('http://localhost:8000/api/connect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        user_name: 'John',
        user_id: 'user-123',
        room_name: 'my-room'
    })
});

const data = await response.json();
// data now contains: { token, url, room, identity, name }
```

---

### Step 2: Add LiveKit Client to Your HTML

```html
<!-- Add this to your HTML <head> -->
<script src="https://unpkg.com/livekit-client/dist/livekit-client.umd.min.js"></script>
```

Or if using npm/modules:
```bash
npm install livekit-client
```

```javascript
import { Room, RoomEvent, Track } from 'livekit-client';
```

---

### Step 3: Create a Room and Connect

```javascript
// Use the token and url from the API response
const room = new LivekitClient.Room();

// Connect using the values from your API
await room.connect(data.url, data.token);
```

**That's the key part!** You use:
- `data.url` → The WebSocket URL
- `data.token` → The authentication token

---

### Step 4: Enable Your Microphone

```javascript
// Enable microphone so you can talk
await room.localParticipant.setMicrophoneEnabled(true);
```

---

### Step 5: Listen for Agent's Audio

```javascript
// Listen for when the agent speaks back
room.on(LivekitClient.RoomEvent.TrackSubscribed, (track) => {
    if (track.kind === LivekitClient.Track.Kind.Audio) {
        // This is the agent's voice
        const audioElement = track.attach();
        document.body.appendChild(audioElement);
        audioElement.play();
    }
});
```

---

## 📱 Complete Working Example

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/livekit-client/dist/livekit-client.umd.min.js"></script>
</head>
<body>
    <button id="connectBtn">Talk to Agent</button>
    
    <script>
        document.getElementById('connectBtn').addEventListener('click', async () => {
            // Step 1: Get connection details from your API
            const response = await fetch('http://localhost:8000/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_name: 'John' })
            });
            
            const data = await response.json();
            
            // Step 2: Create room
            const room = new LivekitClient.Room();
            
            // Step 3: Listen for agent audio
            room.on('trackSubscribed', (track) => {
                if (track.kind === 'audio') {
                    const audioElement = track.attach();
                    document.body.appendChild(audioElement);
                }
            });
            
            // Step 4: Connect using token and URL
            await room.connect(data.url, data.token);
            
            // Step 5: Enable microphone
            await room.localParticipant.setMicrophoneEnabled(true);
            
            console.log('Connected! Start talking.');
        });
    </script>
</body>
</html>
```

---

## 🔄 What Happens Behind the Scenes

```
Your UI
   ↓
1. Call API: POST /api/connect
   ↓
2. Get Response: { token, url, room }
   ↓
3. Connect to LiveKit using token + url
   ↓
4. Agent automatically joins the same room
   ↓
5. Voice communication starts!
   
Your Voice → Agent hears → Agent responds → You hear
```

---

## 🎨 Framework-Specific Examples

### React

```jsx
import { Room } from 'livekit-client';
import { useState } from 'react';

function VoiceAgent() {
    const [connected, setConnected] = useState(false);

    const connect = async () => {
        // Get connection details
        const res = await fetch('http://localhost:8000/api/connect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_name: 'John' })
        });
        
        const data = await res.json();
        
        // Connect
        const room = new Room();
        
        room.on('trackSubscribed', (track) => {
            if (track.kind === 'audio') {
                track.attach();
            }
        });
        
        await room.connect(data.url, data.token);
        await room.localParticipant.setMicrophoneEnabled(true);
        
        setConnected(true);
    };

    return (
        <button onClick={connect}>
            {connected ? 'Connected ✓' : 'Connect'}
        </button>
    );
}
```

---

### Vue.js

```vue
<template>
    <button @click="connect">Talk to Agent</button>
</template>

<script>
import { Room } from 'livekit-client';

export default {
    methods: {
        async connect() {
            // Get connection details
            const res = await fetch('http://localhost:8000/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_name: 'John' })
            });
            
            const data = await res.json();
            
            // Connect
            const room = new Room();
            
            room.on('trackSubscribed', (track) => {
                if (track.kind === 'audio') {
                    track.attach();
                }
            });
            
            await room.connect(data.url, data.token);
            await room.localParticipant.setMicrophoneEnabled(true);
        }
    }
}
</script>
```

---

### Angular

```typescript
import { Component } from '@angular/core';
import { Room } from 'livekit-client';

@Component({
    selector: 'app-voice-agent',
    template: '<button (click)="connect()">Talk to Agent</button>'
})
export class VoiceAgentComponent {
    async connect() {
        // Get connection details
        const response = await fetch('http://localhost:8000/api/connect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_name: 'John' })
        });
        
        const data = await response.json();
        
        // Connect
        const room = new Room();
        
        room.on('trackSubscribed', (track: any) => {
            if (track.kind === 'audio') {
                track.attach();
            }
        });
        
        await room.connect(data.url, data.token);
        await room.localParticipant.setMicrophoneEnabled(true);
    }
}
```

---

## 📱 Mobile Integration

### iOS (Swift)

```swift
import LiveKit

// Get connection details from your API
let url = URL(string: "http://localhost:8000/api/connect")!
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.setValue("application/json", forHTTPHeaderField: "Content-Type")

let body = ["user_name": "John"]
request.httpBody = try? JSONSerialization.data(withJSONObject: body)

let (data, _) = try await URLSession.shared.data(for: request)
let response = try JSONDecoder().decode(ConnectResponse.self, from: data)

// Connect to LiveKit
let room = Room()
try await room.connect(url: response.url, token: response.token)

// Enable microphone
try await room.localParticipant.setMicrophone(enabled: true)
```

---

### Android (Kotlin)

```kotlin
// Get connection details from your API
val client = OkHttpClient()
val json = """{"user_name": "John"}"""
val body = json.toRequestBody("application/json".toMediaType())

val request = Request.Builder()
    .url("http://localhost:8000/api/connect")
    .post(body)
    .build()

val response = client.newCall(request).execute()
val data = JSONObject(response.body?.string())

val token = data.getString("token")
val url = data.getString("url")

// Connect to LiveKit
val room = LiveKit.create(applicationContext)
room.connect(url, token)

// Enable microphone
room.localParticipant.setMicrophoneEnabled(true)
```

---

## 🔍 Understanding Each Field

| Field | Purpose | How to Use |
|-------|---------|------------|
| `token` | Authentication | Pass to `room.connect(url, token)` |
| `url` | LiveKit server | Pass to `room.connect(url, token)` |
| `room` | Room name | For reference/display only |
| `identity` | Your user ID | For reference/display only |
| `name` | Display name | For reference/display only |

**Only `token` and `url` are required to connect!**

---

## ✅ Checklist

- [ ] API returns `token` and `url`
- [ ] LiveKit client SDK installed
- [ ] Room created: `new Room()`
- [ ] Connected: `room.connect(url, token)`
- [ ] Microphone enabled: `setMicrophoneEnabled(true)`
- [ ] Listening for audio: `room.on('trackSubscribed', ...)`

---

## 🐛 Troubleshooting

### "Room not found"
- Make sure agent is running: `uv run python src/agent.py dev`

### "Token invalid"
- Token expires in 6 hours - get a new one from the API

### "No audio"
- Check browser permissions for microphone
- Check `track.kind === 'audio'` in event listener

### "Connection failed"
- Check unified API is running: `uv run python unified_api.py`
- Check `data.url` and `data.token` are not empty

---

## 🎉 That's It!

You now know exactly how to use the API response in your UI. The key is:

1. **Call API** → Get `token` and `url`
2. **Connect** → `room.connect(url, token)`
3. **Enable mic** → `setMicrophoneEnabled(true)`
4. **Listen** → Handle `trackSubscribed` event

**Open `complete_ui_example.html` to see a working example!**

