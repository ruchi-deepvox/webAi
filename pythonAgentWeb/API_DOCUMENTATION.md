# Voice Agent - Unified API Documentation

## Overview

This unified API allows you to easily integrate the LiveKit voice agent into **any frontend** with a single endpoint.

**Base URL:** `http://localhost:8000`

---

## Quick Start

### 1. Start the Unified API Server

```bash
cd pythonAgentWeb
uv run python unified_api.py
```

### 2. Start the Voice Agent

```bash
cd pythonAgentWeb
uv run python src/agent.py dev
```

### 3. Call the API from Your Frontend

```javascript
const response = await fetch('http://localhost:8000/api/connect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
});

const { token, url, room } = await response.json();

// Use token and url with LiveKit client
const room = new LivekitClient.Room();
await room.connect(url, token);
await room.localParticipant.setMicrophoneEnabled(true);
```

---

## Main Endpoint

### `POST /api/connect`

**Connect to the voice agent - this is the main endpoint you'll use!**

#### Request

```http
POST /api/connect HTTP/1.1
Content-Type: application/json

{
    "room_name": "my-room",      // optional
    "user_id": "user-123",        // optional
    "user_name": "John Doe"       // optional
}
```

#### Response

```json
{
    "success": true,
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "url": "wss://voice-4luxbgpy.livekit.cloud",
    "room": "my-room",
    "identity": "user-123",
    "name": "John Doe"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `room_name` | string | No | Custom room name. Auto-generated if not provided |
| `user_id` | string | No | User's unique identifier. Auto-generated if not provided |
| `user_name` | string | No | User's display name. Defaults to "User" |

---

## Additional Endpoints

### `GET /api/health`

Check API health and service status.

#### Response

```json
{
    "success": true,
    "status": "healthy",
    "services": {
        "token_server": "healthy",
        "livekit_configured": true,
        "api_keys": {
            "openai": true,
            "assemblyai": true,
            "cartesia": true
        }
    }
}
```

---

### `GET /api/config`

Get API configuration (without sensitive data).

#### Response

```json
{
    "success": true,
    "config": {
        "livekit_url": "wss://voice-4luxbgpy.livekit.cloud",
        "stt_provider": "AssemblyAI",
        "stt_model": "universal-streaming",
        "llm_provider": "OpenAI",
        "llm_model": "gpt-4.1-mini",
        "tts_provider": "Cartesia",
        "tts_model": "sonic-3"
    }
}
```

---

### `GET /api/rooms`

List all active rooms.

#### Response

```json
{
    "success": true,
    "rooms": [
        {
            "name": "room-1",
            "num_participants": 2,
            "creation_time": 1234567890,
            "sid": "RM_..."
        }
    ]
}
```

---

### `GET /api/room/<room_name>/participants`

List participants in a specific room.

#### Response

```json
{
    "success": true,
    "room": "my-room",
    "participants": [
        {
            "identity": "user-123",
            "name": "John Doe",
            "sid": "PA_...",
            "state": "ACTIVE",
            "is_publisher": true
        }
    ]
}
```

---

### `POST /api/room/<room_name>/disconnect`

Disconnect a room (removes all participants).

#### Response

```json
{
    "success": true,
    "message": "Room my-room disconnected"
}
```

---

## Integration Examples

### Vanilla JavaScript

```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://unpkg.com/livekit-client/dist/livekit-client.umd.min.js"></script>
</head>
<body>
    <button id="connectBtn">Connect to Voice Agent</button>
    
    <script>
        document.getElementById('connectBtn').addEventListener('click', async () => {
            // Step 1: Get connection details from API
            const response = await fetch('http://localhost:8000/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_name: 'Web User'
                })
            });
            
            const data = await response.json();
            
            // Step 2: Connect to LiveKit
            const room = new LivekitClient.Room();
            
            // Step 3: Listen for agent audio
            room.on('trackSubscribed', (track) => {
                if (track.kind === 'audio') {
                    const audioElement = track.attach();
                    document.body.appendChild(audioElement);
                }
            });
            
            // Step 4: Connect and enable microphone
            await room.connect(data.url, data.token);
            await room.localParticipant.setMicrophoneEnabled(true);
            
            console.log('Connected! Start talking.');
        });
    </script>
</body>
</html>
```

---

### React Example

```jsx
import { Room } from 'livekit-client';
import { useState, useEffect } from 'react';

function VoiceAgentButton() {
    const [connected, setConnected] = useState(false);
    const [room, setRoom] = useState(null);

    const connect = async () => {
        try {
            // Call unified API
            const response = await fetch('http://localhost:8000/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_name: 'React User'
                })
            });

            const data = await response.json();

            // Connect to LiveKit
            const newRoom = new Room();
            
            newRoom.on('trackSubscribed', (track) => {
                if (track.kind === 'audio') {
                    track.attach();
                }
            });

            await newRoom.connect(data.url, data.token);
            await newRoom.localParticipant.setMicrophoneEnabled(true);

            setRoom(newRoom);
            setConnected(true);
        } catch (error) {
            console.error('Connection failed:', error);
        }
    };

    const disconnect = async () => {
        if (room) {
            await room.disconnect();
            setRoom(null);
            setConnected(false);
        }
    };

    return (
        <div>
            {!connected ? (
                <button onClick={connect}>Connect to Voice Agent</button>
            ) : (
                <button onClick={disconnect}>Disconnect</button>
            )}
        </div>
    );
}

export default VoiceAgentButton;
```

---

### Vue.js Example

```vue
<template>
    <button @click="toggleConnection">
        {{ connected ? 'Disconnect' : 'Connect to Voice Agent' }}
    </button>
</template>

<script>
import { Room } from 'livekit-client';

export default {
    data() {
        return {
            connected: false,
            room: null
        };
    },
    methods: {
        async connect() {
            const response = await fetch('http://localhost:8000/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_name: 'Vue User'
                })
            });

            const data = await response.json();

            this.room = new Room();
            
            this.room.on('trackSubscribed', (track) => {
                if (track.kind === 'audio') {
                    track.attach();
                }
            });

            await this.room.connect(data.url, data.token);
            await this.room.localParticipant.setMicrophoneEnabled(true);

            this.connected = true;
        },
        async disconnect() {
            if (this.room) {
                await this.room.disconnect();
                this.room = null;
                this.connected = false;
            }
        },
        toggleConnection() {
            if (this.connected) {
                this.disconnect();
            } else {
                this.connect();
            }
        }
    }
};
</script>
```

---

### Python Example

```python
import requests
from livekit import rtc

# Step 1: Get connection details
response = requests.post('http://localhost:8000/api/connect', json={
    'user_name': 'Python User'
})

data = response.json()

# Step 2: Connect with LiveKit Python SDK
async def connect_to_agent():
    room = rtc.Room()
    
    # Listen for audio tracks
    @room.on("track_subscribed")
    def on_track_subscribed(track, publication, participant):
        if track.kind == rtc.TrackKind.KIND_AUDIO:
            print("Agent audio received!")
    
    # Connect
    await room.connect(data['url'], data['token'])
    
    # Publish microphone
    source = rtc.AudioSource(24000, 1)
    track = rtc.LocalAudioTrack.create_audio_track("microphone", source)
    await room.local_participant.publish_track(track)

# Run
import asyncio
asyncio.run(connect_to_agent())
```

---

### cURL Example

```bash
# Get connection details
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"user_name": "CLI User"}'

# Check health
curl http://localhost:8000/api/health

# List rooms
curl http://localhost:8000/api/rooms

# Get config
curl http://localhost:8000/api/config
```

---

## Error Handling

All endpoints return a consistent error format:

```json
{
    "success": false,
    "error": "Error description here"
}
```

HTTP Status Codes:
- `200 OK` - Request successful
- `500 Internal Server Error` - Server error (check agent is running)

---

## CORS Configuration

The API has CORS enabled for all origins, making it easy to integrate from any domain during development.

For production, you should restrict CORS to your specific domain.

---

## Security Notes

1. **This API is for development** - For production, implement proper authentication
2. **JWT tokens** are short-lived and room-specific
3. **API keys** are stored in `.env.local` and never exposed to clients
4. **Token generation** happens server-side only

---

## Testing

### Test with the Example Page

1. Start the unified API:
   ```bash
   uv run python unified_api.py
   ```

2. Start the agent:
   ```bash
   uv run python src/agent.py dev
   ```

3. Open the example:
   ```bash
   start example_integration.html
   ```

---

## Troubleshooting

### "Connection failed"
- Check if unified API is running on port 8000
- Check if voice agent is running
- Verify `.env.local` has correct credentials

### "No audio"
- Check browser microphone permissions
- Check browser console for errors
- Verify agent terminal shows "publishing audio"

### "API not responding"
- Check port 8000 is not in use
- Restart the unified API server
- Check firewall settings

---

## Port Configuration

| Service | Port | URL |
|---------|------|-----|
| Unified API | 8000 | http://localhost:8000 |
| Voice Agent | N/A | Connects to LiveKit Cloud |
| LiveKit Cloud | 443 | wss://voice-4luxbgpy.livekit.cloud |

---

## Need Help?

- Check API documentation: http://localhost:8000/api
- Check health status: http://localhost:8000/api/health
- Review example integration: `example_integration.html`
- Check connection architecture: `CONNECTION_ARCHITECTURE.md`

