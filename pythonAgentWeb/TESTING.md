# Testing Your LiveKit Agent

## Quick Test Methods

### Method 1: Use LiveKit Playground (Easiest for Voice Testing)

1. **Start your agent in dev mode:**
   ```bash
   cd pythonAgentWeb
   uv run python src/agent.py dev
   ```

2. **Go to LiveKit Cloud:**
   - Visit: https://cloud.livekit.io/
   - Sign in to your account
   - Click on "Agents" in the sidebar
   - Click "Test in Playground"
   - Enable your microphone and start talking!

The agent should automatically join the room and respond to your voice.

### Method 2: Use the Test Connection Script

Run the automated test script (while your agent is running in another terminal):

```bash
cd pythonAgentWeb
uv run python test_connection.py
```

This script will:
- Create a test room
- Verify the agent can connect
- List participants
- Clean up the room

### Method 3: Build a Simple Web Client

You can create a simple web page to test your agent. Check out the LiveKit examples:
- https://github.com/livekit/agents-playground

## Testing Voice Interactions

When testing voice interactions, try these sample conversations:

### Basic Greeting
- **You:** "Hello, how are you?"
- **Expected:** Friendly greeting response

### Knowledge Questions
- **You:** "What is the capital of France?"
- **Expected:** Accurate factual response

### Grounding Test (Does NOT hallucinate)
- **You:** "What's my favorite color?"
- **Expected:** Should say it doesn't have access to that information

### Multi-turn Conversation
- **You:** "Tell me about Python programming"
- **Agent:** *responds*
- **You:** "What are its main benefits?"
- **Expected:** Maintains context from previous turn

## Troubleshooting

### Agent Not Connecting
- Check your `.env.local` file has valid credentials:
  - `LIVEKIT_URL`
  - `LIVEKIT_API_KEY`
  - `LIVEKIT_API_SECRET`

### No Audio
- Make sure your microphone is enabled in your browser/system
- Check browser permissions for microphone access

### Encoding Errors on Windows
If you see `UnicodeEncodeError`, run with UTF-8 encoding:
```bash
$env:PYTHONIOENCODING='utf-8'; uv run python src/agent.py dev
```

## Next Steps

Once basic testing works:

1. **Add custom tools** - Modify `agent.py` to add function tools
2. **Write unit tests** - Add tests to `tests/test_agent.py`
3. **Deploy to production** - Use the provided Dockerfile
4. **Monitor performance** - Check LiveKit Cloud dashboard

## API Keys for Testing

You'll need API keys for the services used:

- **OpenAI** (for GPT-4.1-mini): Set `OPENAI_API_KEY` in `.env.local`
- **AssemblyAI** (for STT): Set `ASSEMBLYAI_API_KEY` in `.env.local`
- **Cartesia** (for TTS): Set `CARTESIA_API_KEY` in `.env.local`

Without these, the agent won't be able to process voice or generate responses.

