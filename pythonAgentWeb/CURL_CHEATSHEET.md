# 🚀 Curl Cheat Sheet - Voice Agent API

## Quick Start

**Base URL:** `http://localhost:8000`

---

## 🔥 Main Command - Connect to Voice Agent

```bash
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"user_name": "John Doe"}'
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "url": "wss://voice-4luxbgpy.livekit.cloud",
  "room": "room-123456",
  "identity": "user-123456",
  "name": "John Doe"
}
```

---

## 📋 All Endpoints

### 1. Connect to Agent ⭐ (MAIN)

```bash
# Full parameters
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{
    "room_name": "my-custom-room",
    "user_id": "user-123",
    "user_name": "John Doe"
  }'

# Minimal (auto-generates room and user)
curl -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{}'

# Windows PowerShell
Invoke-RestMethod -Uri http://localhost:8000/api/connect `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"user_name": "John"}'
```

---

### 2. Health Check

```bash
curl http://localhost:8000/api/health

# Pretty print with jq
curl -s http://localhost:8000/api/health | jq '.'

# Windows PowerShell
(Invoke-RestMethod http://localhost:8000/api/health) | ConvertTo-Json
```

**Response:**
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

### 3. Get Configuration

```bash
curl http://localhost:8000/api/config

# Windows PowerShell
Invoke-RestMethod http://localhost:8000/api/config
```

**Response:**
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

### 4. List All Rooms

```bash
curl http://localhost:8000/api/rooms

# Windows PowerShell
Invoke-RestMethod http://localhost:8000/api/rooms
```

**Response:**
```json
{
  "success": true,
  "rooms": [
    {
      "name": "room-123456",
      "num_participants": 2,
      "creation_time": 1234567890,
      "sid": "RM_..."
    }
  ]
}
```

---

### 5. List Participants in Room

```bash
# Replace 'my-room' with your room name
curl http://localhost:8000/api/room/my-room/participants

# Windows PowerShell
Invoke-RestMethod http://localhost:8000/api/room/my-room/participants
```

**Response:**
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

### 6. Disconnect Room

```bash
curl -X POST http://localhost:8000/api/room/my-room/disconnect

# Windows PowerShell
Invoke-RestMethod -Uri http://localhost:8000/api/room/my-room/disconnect -Method Post
```

**Response:**
```json
{
  "success": true,
  "message": "Room my-room disconnected"
}
```

---

### 7. API Documentation

```bash
curl http://localhost:8000/api

# Or open in browser
start http://localhost:8000/api  # Windows
open http://localhost:8000/api   # macOS
xdg-open http://localhost:8000/api  # Linux
```

---

## 🔄 Complete Workflow Example

```bash
# Step 1: Check if API is healthy
curl http://localhost:8000/api/health

# Step 2: Connect to agent and get credentials
RESPONSE=$(curl -s -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"user_name": "Test User"}')

# Step 3: Extract values (using jq)
TOKEN=$(echo $RESPONSE | jq -r '.token')
URL=$(echo $RESPONSE | jq -r '.url')
ROOM=$(echo $RESPONSE | jq -r '.room')

echo "Token: $TOKEN"
echo "URL: $URL"
echo "Room: $ROOM"

# Step 4: Use these values with LiveKit client (in your app)
# Now use TOKEN and URL to connect with LiveKit SDK

# Step 5: List rooms to see your active room
curl http://localhost:8000/api/rooms

# Step 6: List participants in your room
curl http://localhost:8000/api/room/$ROOM/participants

# Step 7: Disconnect when done
curl -X POST http://localhost:8000/api/room/$ROOM/disconnect
```

---

## 💻 Platform-Specific Examples

### Windows PowerShell

```powershell
# Connect
$response = Invoke-RestMethod -Uri http://localhost:8000/api/connect `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"user_name": "John"}'

# Extract values
$token = $response.token
$url = $response.url
$room = $response.room

Write-Host "Token: $token"
Write-Host "URL: $url"
Write-Host "Room: $room"
```

### Linux/Mac (Bash)

```bash
#!/bin/bash

# Connect
response=$(curl -s -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"user_name": "John"}')

# Extract values
token=$(echo $response | jq -r '.token')
url=$(echo $response | jq -r '.url')
room=$(echo $response | jq -r '.room')

echo "Token: $token"
echo "URL: $url"
echo "Room: $room"
```

---

## 🧪 Testing Scripts

### Run All Tests (Windows)

```powershell
.\test_api.ps1
```

### Run All Tests (Linux/Mac)

```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 🔑 Using the Response in Your App

After getting the response from `/api/connect`, use it with LiveKit client:

### JavaScript

```javascript
// Get connection details
const response = await fetch('http://localhost:8000/api/connect', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_name: 'John' })
});

const { token, url } = await response.json();

// Connect with LiveKit
import { Room } from 'livekit-client';
const room = new Room();
await room.connect(url, token);
await room.localParticipant.setMicrophoneEnabled(true);
```

### Python

```python
import requests
from livekit import rtc

# Get connection details
response = requests.post('http://localhost:8000/api/connect', 
    json={'user_name': 'John'})
data = response.json()

# Connect with LiveKit
room = rtc.Room()
await room.connect(data['url'], data['token'])
```

---

## 🐛 Debugging

### Check if API is running

```bash
curl http://localhost:8000/api/health
```

If this fails, start the API:
```bash
cd pythonAgentWeb
uv run python unified_api.py
```

### Check if Agent is running

Make sure your voice agent is running:
```bash
cd pythonAgentWeb
uv run python src/agent.py dev
```

### View detailed error

```bash
# Add -v flag for verbose output
curl -v -X POST http://localhost:8000/api/connect \
  -H "Content-Type: application/json" \
  -d '{"user_name": "John"}'
```

---

## 📊 Response Status Codes

| Code | Status | Meaning |
|------|--------|---------|
| 200 | OK | Request successful |
| 500 | Internal Server Error | Check if agent is running |

---

## 🔒 Security Notes

- This API is designed for **development/testing**
- For production, add authentication (API keys, OAuth, etc.)
- Restrict CORS to your domain
- Use HTTPS in production

---

## 🌐 CORS

The API has CORS enabled for all origins (`*`) for easy development.

To test from different domains:
```bash
curl -H "Origin: http://example.com" http://localhost:8000/api/connect
```

---

## ⚡ Quick Copy-Paste Commands

```bash
# Test connection
curl -X POST http://localhost:8000/api/connect -H "Content-Type: application/json" -d '{"user_name": "Test"}'

# Check health
curl http://localhost:8000/api/health

# List rooms
curl http://localhost:8000/api/rooms

# Get config
curl http://localhost:8000/api/config
```

---

## 📞 Support

- **API Docs:** http://localhost:8000/api
- **Health Check:** http://localhost:8000/api/health
- **Full Docs:** See `API_DOCUMENTATION.md`
- **Architecture:** See `CONNECTION_ARCHITECTURE.md`

---

## 🎯 Next Steps

1. Test the API with curl
2. Integrate into your UI
3. Add error handling
4. Customize room names and user IDs
5. Deploy to production (with proper security)

**You're all set!** 🚀

