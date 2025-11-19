# Frontend-Backend Connection Architecture

## Overview

This document explains how the frontend (web UI) connects to the backend (voice agent).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                           │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  simple_tester.html (Frontend)                        │  │
│  │  - User interface                                     │  │
│  │  - LiveKit Client SDK                                 │  │
│  │  - Audio capture/playback                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │
                           │ Step 1: Request Auth Token
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Token Server (localhost:5000)                  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  token_server.py                                      │  │
│  │  - Flask web server                                   │  │
│  │  - Generates JWT tokens                               │  │
│  │  - Endpoint: GET /token?room=xxx&identity=yyy        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ Step 2: Return Token + URL
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  LiveKit Cloud Infrastructure               │
│                  (wss://voice-4luxbgpy.livekit.cloud)       │
│                                                             │
│  - WebRTC Media Server                                      │
│  - Real-time Audio/Video Routing                            │
│  - Room Management                                          │
│                                                             │
│         Browser (web-user) ←──RTC──→ Agent (agent-xxx)     │
└─────────────────────────────────────────────────────────────┘
                           ↑
                           │ Step 3: Agent Auto-joins Room
                           │
┌─────────────────────────────────────────────────────────────┐
│              Voice Agent Backend                            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  src/agent.py                                         │  │
│  │  - LiveKit Agent Server                               │  │
│  │  - Monitors for new rooms                             │  │
│  │  - Auto-joins when room created                       │  │
│  │  - STT → LLM → TTS pipeline                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Connected Services:                                        │
│  - AssemblyAI (Speech-to-Text)                             │
│  - OpenAI (GPT-4.1-mini for LLM)                           │
│  - Cartesia (Text-to-Speech)                               │
└─────────────────────────────────────────────────────────────┘
```

## Connection Flow Step-by-Step

### Step 1: User Opens Frontend
```javascript
// File: simple_tester.html
window.connect = async function() {
    // 1. Get room name from input or auto-generate
    let roomName = `test-room-${Date.now()}`;
    
    // 2. Request token from token server
    const response = await fetch(`http://localhost:5000/token?room=${roomName}&identity=web-user`);
    const { token, url } = await response.json();
    // ...
}
```

### Step 2: Token Server Generates Auth Token
```python
# File: token_server.py
@app.route('/token', methods=['GET'])
def generate_token():
    room_name = request.args.get('room')
    identity = request.args.get('identity')
    
    # Create JWT token with permissions
    token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    token.with_identity(identity)
    token.with_grants(
        api.VideoGrants(
            room_join=True,
            room=room_name,
            can_publish=True,
            can_subscribe=True,
        )
    )
    
    return jsonify({
        'token': token.to_jwt(),
        'url': LIVEKIT_URL,
        'room': room_name
    })
```

### Step 3: Frontend Connects to LiveKit
```javascript
// File: simple_tester.html
// Create LiveKit room
room = new Room({
    adaptiveStream: true,
    dynacast: true,
});

// Connect using token
await room.connect(url, token);

// Enable microphone
await room.localParticipant.setMicrophoneEnabled(true);
```

### Step 4: Agent Auto-Joins Room
```python
# File: src/agent.py
@server.rtc_session()
async def my_agent(ctx: JobContext):
    # Set up voice pipeline
    session = AgentSession(
        stt=inference.STT(model="assemblyai/universal-streaming"),
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        tts=inference.TTS(model="cartesia/sonic-3", voice="..."),
        # ...
    )
    
    # Start session and connect to room
    await session.start(agent=Assistant(), room=ctx.room)
    await ctx.connect()  # Agent joins the room
```

### Step 5: Real-time Communication
```
User speaks → Browser captures audio → LiveKit Cloud
                                           ↓
                                    Agent receives audio
                                           ↓
                                    AssemblyAI (STT)
                                           ↓
                                    OpenAI GPT-4.1 (LLM)
                                           ↓
                                    Cartesia (TTS)
                                           ↓
                                    Agent sends audio → LiveKit Cloud
                                                           ↓
                                                    Browser plays audio
```

## Key Files and Their Roles

| File | Type | Purpose | Port/URL |
|------|------|---------|----------|
| `simple_tester.html` | Frontend | User interface, audio I/O | Browser |
| `token_server.py` | Backend | Authentication service | localhost:5000 |
| `src/agent.py` | Backend | AI voice processing | Connects to LiveKit |
| `.env.local` | Config | API keys and credentials | N/A |

## API Endpoints

### Token Server API

#### `GET /token`
Generates an authentication token for LiveKit connection.

**Parameters:**
- `room` (string, optional): Room name to join
- `identity` (string, optional): User identity

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1...",
  "url": "wss://voice-4luxbgpy.livekit.cloud",
  "room": "test-room-1234567890"
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Security Notes

1. **Token Server** runs locally and uses your LiveKit API credentials from `.env.local`
2. **JWT Tokens** are short-lived and room-specific
3. **CORS** is enabled on the token server for local development
4. **In Production**: Token server should be deployed securely, not exposed publicly

## Running the System

### Required Services

1. **Token Server:**
   ```bash
   cd pythonAgentWeb
   uv run python token_server.py
   ```

2. **Voice Agent:**
   ```bash
   cd pythonAgentWeb
   uv run python src/agent.py dev
   ```

3. **Frontend:**
   - Open `simple_tester.html` in browser
   - Click "Connect & Talk"

## Environment Variables

All credentials are stored in `pythonAgentWeb/.env.local`:

```bash
# LiveKit
LIVEKIT_URL=wss://voice-4luxbgpy.livekit.cloud
LIVEKIT_API_KEY=APIxxxxxxxxx
LIVEKIT_API_SECRET=xxxxxxxxxx

# AI Services
OPENAI_API_KEY=sk-proj-xxxxxxxxxx
ASSEMBLYAI_API_KEY=xxxxxxxxxx
CARTESIA_API_KEY=sk_car_xxxxxxxxxx
ELEVENLABS_API_KEY=sk_xxxxxxxxxx  # If using ElevenLabs
```

## Debugging

### Check Connection Status

1. **Token Server:**
   ```bash
   curl http://localhost:5000/health
   ```

2. **Frontend Console:**
   - Press F12 in browser
   - Check Console tab for errors

3. **Agent Logs:**
   - Check terminal where agent is running
   - Look for "participant joined" messages

## Network Diagram

```
┌──────────┐     HTTP      ┌──────────────┐
│ Browser  │──────────────►│ Token Server │
│          │◄──────────────│ (port 5000)  │
└──────────┘   JWT Token   └──────────────┘
      │
      │ WebRTC (WSS)
      ↓
┌─────────────────┐
│  LiveKit Cloud  │
│  (WebRTC Media) │
└─────────────────┘
      ↑
      │ WebRTC (WSS)
      │
┌──────────┐
│  Agent   │
│ (Python) │
└──────────┘
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, JavaScript, LiveKit Client SDK |
| Backend Auth | Python Flask, LiveKit Server SDK |
| Backend Agent | Python, LiveKit Agents SDK |
| Media Transport | WebRTC over WSS |
| Infrastructure | LiveKit Cloud |
| AI Services | AssemblyAI, OpenAI, Cartesia |

## Troubleshooting

### "Connection Failed"
- Check token server is running (port 5000)
- Check agent is running (`uv run python src/agent.py dev`)
- Verify `.env.local` has correct credentials

### "No Audio"
- Check browser microphone permissions
- Check browser autoplay policy
- Look for "Audio play error" in activity log

### "Agent Not Responding"
- Check agent terminal for errors
- Verify all API keys in `.env.local`
- Check LiveKit Cloud dashboard for room activity

