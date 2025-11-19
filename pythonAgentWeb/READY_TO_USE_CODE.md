# 🚀 Ready-to-Use Code - Voice Agent Integration

## Copy-Paste Into Your UI

---

## 📱 Vanilla JavaScript (Pure HTML)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Voice Agent</title>
</head>
<body>
    <button id="connectBtn">Connect to Agent</button>
    <button id="disconnectBtn" disabled>Disconnect</button>
    <div id="status">Disconnected</div>

    <script type="module">
        import { Room, RoomEvent, Track } from 'https://cdn.jsdelivr.net/npm/livekit-client/dist/livekit-client.esm.mjs';
        
        let room = null;
        const API_URL = 'http://localhost:8000/api/connect';

        // Connect Function
        async function connect() {
            try {
                // Clean up existing connection
                if (room) {
                    await disconnect();
                    await new Promise(r => setTimeout(r, 500));
                }

                document.getElementById('status').textContent = 'Connecting...';

                // Get token from API
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_name: 'User',
                        room_name: `room-${Date.now()}`
                    })
                });

                const { token, url } = await response.json();

                // Create and connect room
                room = new Room();

                // Listen for agent audio
                room.on(RoomEvent.TrackSubscribed, (track) => {
                    if (track.kind === Track.Kind.Audio) {
                        track.attach();
                    }
                });

                room.on(RoomEvent.Connected, () => {
                    document.getElementById('status').textContent = 'Connected - Start talking!';
                });

                // Connect
                await room.connect(url, token);
                await room.localParticipant.setMicrophoneEnabled(true);

                // Update UI
                document.getElementById('connectBtn').disabled = true;
                document.getElementById('disconnectBtn').disabled = false;

            } catch (error) {
                console.error('Connection error:', error);
                document.getElementById('status').textContent = 'Connection failed';
            }
        }

        // Disconnect Function
        async function disconnect() {
            if (room) {
                await room.localParticipant.setMicrophoneEnabled(false);
                await room.disconnect();
                room = null;
                
                document.getElementById('status').textContent = 'Disconnected';
                document.getElementById('connectBtn').disabled = false;
                document.getElementById('disconnectBtn').disabled = true;
            }
        }

        // Attach event listeners
        document.getElementById('connectBtn').addEventListener('click', connect);
        document.getElementById('disconnectBtn').addEventListener('click', disconnect);
    </script>
</body>
</html>
```

---

## ⚛️ React

```jsx
import { Room, RoomEvent, Track } from 'livekit-client';
import { useState, useRef } from 'react';

function VoiceAgent() {
    const [connected, setConnected] = useState(false);
    const [status, setStatus] = useState('Disconnected');
    const roomRef = useRef(null);

    const connect = async () => {
        try {
            // Clean up existing connection
            if (roomRef.current) {
                await disconnect();
                await new Promise(r => setTimeout(r, 500));
            }

            setStatus('Connecting...');

            // Get token from API
            const response = await fetch('http://localhost:8000/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_name: 'User',
                    room_name: `room-${Date.now()}`
                })
            });

            const { token, url } = await response.json();

            // Create room
            const room = new Room();
            roomRef.current = room;

            // Listen for agent audio
            room.on(RoomEvent.TrackSubscribed, (track) => {
                if (track.kind === Track.Kind.Audio) {
                    track.attach();
                }
            });

            room.on(RoomEvent.Connected, () => {
                setStatus('Connected - Start talking!');
                setConnected(true);
            });

            // Connect
            await room.connect(url, token);
            await room.localParticipant.setMicrophoneEnabled(true);

        } catch (error) {
            console.error('Connection error:', error);
            setStatus('Connection failed');
            setConnected(false);
        }
    };

    const disconnect = async () => {
        if (roomRef.current) {
            await roomRef.current.localParticipant.setMicrophoneEnabled(false);
            await roomRef.current.disconnect();
            roomRef.current = null;
            
            setStatus('Disconnected');
            setConnected(false);
        }
    };

    return (
        <div>
            <h2>Voice Agent</h2>
            <p>Status: {status}</p>
            <button onClick={connect} disabled={connected}>
                Connect to Agent
            </button>
            <button onClick={disconnect} disabled={!connected}>
                Disconnect
            </button>
        </div>
    );
}

export default VoiceAgent;
```

---

## 🟢 Vue.js 3 (Composition API)

```vue
<template>
    <div>
        <h2>Voice Agent</h2>
        <p>Status: {{ status }}</p>
        <button @click="connect" :disabled="connected">
            Connect to Agent
        </button>
        <button @click="disconnect" :disabled="!connected">
            Disconnect
        </button>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { Room, RoomEvent, Track } from 'livekit-client';

const connected = ref(false);
const status = ref('Disconnected');
const room = ref(null);

const connect = async () => {
    try {
        // Clean up existing connection
        if (room.value) {
            await disconnect();
            await new Promise(r => setTimeout(r, 500));
        }

        status.value = 'Connecting...';

        // Get token from API
        const response = await fetch('http://localhost:8000/api/connect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                user_name: 'User',
                room_name: `room-${Date.now()}`
            })
        });

        const { token, url } = await response.json();

        // Create room
        room.value = new Room();

        // Listen for agent audio
        room.value.on(RoomEvent.TrackSubscribed, (track) => {
            if (track.kind === Track.Kind.Audio) {
                track.attach();
            }
        });

        room.value.on(RoomEvent.Connected, () => {
            status.value = 'Connected - Start talking!';
            connected.value = true;
        });

        // Connect
        await room.value.connect(url, token);
        await room.value.localParticipant.setMicrophoneEnabled(true);

    } catch (error) {
        console.error('Connection error:', error);
        status.value = 'Connection failed';
        connected.value = false;
    }
};

const disconnect = async () => {
    if (room.value) {
        await room.value.localParticipant.setMicrophoneEnabled(false);
        await room.value.disconnect();
        room.value = null;
        
        status.value = 'Disconnected';
        connected.value = false;
    }
};
</script>
```

---

## 🅰️ Angular

```typescript
// voice-agent.component.ts
import { Component } from '@angular/core';
import { Room, RoomEvent, Track } from 'livekit-client';

@Component({
    selector: 'app-voice-agent',
    template: `
        <div>
            <h2>Voice Agent</h2>
            <p>Status: {{ status }}</p>
            <button (click)="connect()" [disabled]="connected">
                Connect to Agent
            </button>
            <button (click)="disconnect()" [disabled]="!connected">
                Disconnect
            </button>
        </div>
    `
})
export class VoiceAgentComponent {
    connected = false;
    status = 'Disconnected';
    private room: Room | null = null;

    async connect() {
        try {
            // Clean up existing connection
            if (this.room) {
                await this.disconnect();
                await new Promise(r => setTimeout(r, 500));
            }

            this.status = 'Connecting...';

            // Get token from API
            const response = await fetch('http://localhost:8000/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_name: 'User',
                    room_name: `room-${Date.now()}`
                })
            });

            const data = await response.json();

            // Create room
            this.room = new Room();

            // Listen for agent audio
            this.room.on(RoomEvent.TrackSubscribed, (track: any) => {
                if (track.kind === Track.Kind.Audio) {
                    track.attach();
                }
            });

            this.room.on(RoomEvent.Connected, () => {
                this.status = 'Connected - Start talking!';
                this.connected = true;
            });

            // Connect
            await this.room.connect(data.url, data.token);
            await this.room.localParticipant.setMicrophoneEnabled(true);

        } catch (error) {
            console.error('Connection error:', error);
            this.status = 'Connection failed';
            this.connected = false;
        }
    }

    async disconnect() {
        if (this.room) {
            await this.room.localParticipant.setMicrophoneEnabled(false);
            await this.room.disconnect();
            this.room = null;
            
            this.status = 'Disconnected';
            this.connected = false;
        }
    }
}
```

---

## 📱 React Native

```jsx
import { useState, useRef } from 'react';
import { View, Text, Button } from 'react-native';
import { Room, RoomEvent, Track } from 'livekit-client';

export default function VoiceAgent() {
    const [connected, setConnected] = useState(false);
    const [status, setStatus] = useState('Disconnected');
    const roomRef = useRef(null);

    const connect = async () => {
        try {
            if (roomRef.current) {
                await disconnect();
                await new Promise(r => setTimeout(r, 500));
            }

            setStatus('Connecting...');

            const response = await fetch('http://YOUR_SERVER_IP:8000/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_name: 'Mobile User',
                    room_name: `room-${Date.now()}`
                })
            });

            const { token, url } = await response.json();

            const room = new Room();
            roomRef.current = room;

            room.on(RoomEvent.TrackSubscribed, (track) => {
                if (track.kind === Track.Kind.Audio) {
                    track.attach();
                }
            });

            room.on(RoomEvent.Connected, () => {
                setStatus('Connected!');
                setConnected(true);
            });

            await room.connect(url, token);
            await room.localParticipant.setMicrophoneEnabled(true);

        } catch (error) {
            console.error(error);
            setStatus('Failed');
        }
    };

    const disconnect = async () => {
        if (roomRef.current) {
            await roomRef.current.localParticipant.setMicrophoneEnabled(false);
            await roomRef.current.disconnect();
            roomRef.current = null;
            setStatus('Disconnected');
            setConnected(false);
        }
    };

    return (
        <View>
            <Text>Status: {status}</Text>
            <Button title="Connect" onPress={connect} disabled={connected} />
            <Button title="Disconnect" onPress={disconnect} disabled={!connected} />
        </View>
    );
}
```

---

## 🔥 The Minimal Code (Just 10 Lines!)

```javascript
import { Room } from 'livekit-client';

// Get connection details
const { token, url } = await fetch('http://localhost:8000/api/connect', {
    method: 'POST',
    body: JSON.stringify({ room_name: `room-${Date.now()}` })
}).then(r => r.json());

// Connect
const room = new Room();
room.on('trackSubscribed', track => track.kind === 'audio' && track.attach());
await room.connect(url, token);
await room.localParticipant.setMicrophoneEnabled(true);
```

---

## 📦 Installation

### For React/Vue/Angular

```bash
npm install livekit-client
```

### For HTML (No Install Needed)

```html
<script type="module">
    import { Room } from 'https://cdn.jsdelivr.net/npm/livekit-client/dist/livekit-client.esm.mjs';
</script>
```

---

## ✅ Key Features in This Code:

1. ✅ **Proper Disconnect** - Cleans up before reconnecting
2. ✅ **New Room Each Time** - Fresh connection every time
3. ✅ **Error Handling** - Catches and logs errors
4. ✅ **Audio Autoplay** - Agent voice plays automatically
5. ✅ **Simple API** - Just one POST request

---

## 🔧 Configuration

Change these values to customize:

```javascript
// API URL (change for production)
const API_URL = 'http://localhost:8000/api/connect';

// User details
body: JSON.stringify({
    user_name: 'Your Name',
    user_id: 'custom-id',
    room_name: `room-${Date.now()}` // New room each time
})
```

---

## 🎯 Quick Start

1. **Make sure servers are running:**
   ```bash
   # Terminal 1: API Server
   uv run python unified_api.py
   
   # Terminal 2: Voice Agent
   uv run python src/agent.py dev
   ```

2. **Copy the code for your framework**

3. **Install dependencies** (if needed):
   ```bash
   npm install livekit-client
   ```

4. **That's it!** 🚀

---

## 🐛 Troubleshooting

### "Failed to connect"
- Check API is running: `curl http://localhost:8000/api/health`
- Check agent is running

### "No audio"
- Check browser microphone permissions
- Check console for errors

### "Agent not responding after reconnect"
- Code now handles this! Each connection uses a new room

---

## 📚 Full Examples

- **HTML:** `complete_ui_example.html`
- **Docs:** `API_DOCUMENTATION.md`
- **Curl:** `CURL_CHEATSHEET.md`

