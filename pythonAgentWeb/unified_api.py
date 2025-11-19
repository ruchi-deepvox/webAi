"""
Unified API for LiveKit Voice Agent
Single endpoint to integrate voice agent into any frontend
"""
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from livekit import api
from dotenv import load_dotenv

load_dotenv(".env.local")

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# LiveKit credentials
LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

# =============================================================================
# MAIN API ENDPOINT - Connect to Voice Agent
# =============================================================================

@app.route('/api/connect', methods=['POST'])
def connect_to_agent():
    """
    Main endpoint to connect to the voice agent.
    
    POST /api/connect
    Body: {
        "room_name": "optional-room-name",
        "user_id": "optional-user-id",
        "user_name": "optional-user-name",
        "instructions": "optional-custom-prompt",
        "tts_provider": "cartesia|elevenlabs (optional, default: cartesia)",
        "voice_id": "optional-voice-id"
    }
    
    Returns: {
        "success": true,
        "token": "jwt-token",
        "url": "wss://...",
        "room": "room-name",
        "identity": "user-identity"
    }
    """
    try:
        data = request.json or {}
        
        # Get or generate room name
        room_name = data.get('room_name') or f'room-{int(os.times().elapsed)}'
        
        # Get or generate user identity
        user_id = data.get('user_id') or f'user-{int(os.times().elapsed)}'
        user_name = data.get('user_name') or 'User'
        
        # Get custom instructions (if provided)
        custom_instructions = data.get('instructions')
        
        # Get TTS configuration (if provided)
        tts_provider = data.get('tts_provider', 'cartesia')  # Default to cartesia
        voice_id = data.get('voice_id')  # Optional voice ID
        
        # Generate access token
        token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        token.with_identity(user_id)
        token.with_name(user_name)
        
        # Build metadata
        metadata = {}
        if custom_instructions:
            metadata['instructions'] = custom_instructions
        if tts_provider:
            metadata['tts_provider'] = tts_provider
        if voice_id:
            metadata['voice_id'] = voice_id
        
        # Add metadata to token
        if metadata:
            token.with_metadata(json.dumps(metadata))
        
        token.with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
                can_publish=True,
                can_subscribe=True,
                can_publish_data=True,
            )
        )
        
        jwt_token = token.to_jwt()
        
        response_data = {
            'success': True,
            'token': jwt_token,
            'url': LIVEKIT_URL,
            'room': room_name,
            'identity': user_id,
            'name': user_name,
            'tts_provider': tts_provider
        }
        
        # Include optional parameters in response if provided
        if custom_instructions:
            response_data['instructions'] = custom_instructions
        if voice_id:
            response_data['voice_id'] = voice_id
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =============================================================================
# Additional Helper Endpoints
# =============================================================================

@app.route('/api/rooms', methods=['GET'])
async def list_rooms():
    """
    List all active rooms.
    
    GET /api/rooms
    
    Returns: {
        "success": true,
        "rooms": [
            {"name": "room-1", "num_participants": 2, ...}
        ]
    }
    """
    try:
        lk_api = api.LiveKitAPI(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        rooms = await lk_api.room.list_rooms(api.ListRoomsRequest())
        
        room_list = [
            {
                'name': room.name,
                'num_participants': room.num_participants,
                'creation_time': room.creation_time,
                'sid': room.sid
            }
            for room in rooms.rooms
        ]
        
        await lk_api.aclose()
        
        return jsonify({
            'success': True,
            'rooms': room_list
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/room/<room_name>/participants', methods=['GET'])
async def list_participants(room_name):
    """
    List participants in a specific room.
    
    GET /api/room/<room_name>/participants
    
    Returns: {
        "success": true,
        "participants": [
            {"identity": "user-1", "name": "John", ...}
        ]
    }
    """
    try:
        lk_api = api.LiveKitAPI(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        participants_response = await lk_api.room.list_participants(
            api.ListParticipantsRequest(room=room_name)
        )
        
        participant_list = [
            {
                'identity': p.identity,
                'name': p.name,
                'sid': p.sid,
                'state': str(p.state),
                'is_publisher': p.is_publisher
            }
            for p in participants_response.participants
        ]
        
        await lk_api.aclose()
        
        return jsonify({
            'success': True,
            'room': room_name,
            'participants': participant_list
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/room/<room_name>/disconnect', methods=['POST'])
async def disconnect_from_room(room_name):
    """
    Delete a room (disconnect all participants).
    
    POST /api/room/<room_name>/disconnect
    
    Returns: {
        "success": true,
        "message": "Room disconnected"
    }
    """
    try:
        lk_api = api.LiveKitAPI(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        await lk_api.room.delete_room(api.DeleteRoomRequest(room=room_name))
        await lk_api.aclose()
        
        return jsonify({
            'success': True,
            'message': f'Room {room_name} disconnected'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# =============================================================================
# Configuration Endpoints
# =============================================================================

@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Get API configuration (without sensitive data).
    
    GET /api/config
    
    Returns: {
        "success": true,
        "config": {
            "livekit_url": "wss://...",
            "stt_provider": "AssemblyAI",
            "llm_provider": "OpenAI",
            "tts_provider": "Cartesia"
        }
    }
    """
    return jsonify({
        'success': True,
        'config': {
            'livekit_url': LIVEKIT_URL,
            'stt_provider': 'AssemblyAI',
            'stt_model': 'universal-streaming',
            'llm_provider': 'OpenAI',
            'llm_model': 'gpt-4.1-mini',
            'tts_provider': 'Cartesia',
            'tts_model': 'sonic-3'
        }
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    GET /api/health
    
    Returns: {
        "success": true,
        "status": "healthy",
        "services": {...}
    }
    """
    services = {
        'token_server': 'healthy',
        'livekit_configured': bool(LIVEKIT_URL and LIVEKIT_API_KEY and LIVEKIT_API_SECRET),
        'api_keys': {
            'openai': bool(os.getenv('OPENAI_API_KEY')),
            'assemblyai': bool(os.getenv('ASSEMBLYAI_API_KEY')),
            'cartesia': bool(os.getenv('CARTESIA_API_KEY'))
        }
    }
    
    return jsonify({
        'success': True,
        'status': 'healthy',
        'services': services
    })


# =============================================================================
# Documentation Endpoint
# =============================================================================

@app.route('/', methods=['GET'])
@app.route('/api', methods=['GET'])
def api_docs():
    """
    API Documentation.
    """
    docs = {
        'name': 'LiveKit Voice Agent API',
        'version': '1.0.0',
        'description': 'Unified API for integrating voice agent into any frontend',
        'base_url': request.host_url,
        'endpoints': {
            'POST /api/connect': {
                'description': 'Connect to voice agent (main endpoint)',
                'body': {
                    'room_name': 'string (optional)',
                    'user_id': 'string (optional)',
                    'user_name': 'string (optional)'
                },
                'response': {
                    'success': 'boolean',
                    'token': 'string (JWT)',
                    'url': 'string (LiveKit URL)',
                    'room': 'string',
                    'identity': 'string'
                }
            },
            'GET /api/rooms': {
                'description': 'List all active rooms',
                'response': {
                    'success': 'boolean',
                    'rooms': 'array'
                }
            },
            'GET /api/room/<room_name>/participants': {
                'description': 'List participants in a room',
                'response': {
                    'success': 'boolean',
                    'participants': 'array'
                }
            },
            'POST /api/room/<room_name>/disconnect': {
                'description': 'Disconnect a room',
                'response': {
                    'success': 'boolean',
                    'message': 'string'
                }
            },
            'GET /api/config': {
                'description': 'Get API configuration',
                'response': {
                    'success': 'boolean',
                    'config': 'object'
                }
            },
            'GET /api/health': {
                'description': 'Health check',
                'response': {
                    'success': 'boolean',
                    'status': 'string',
                    'services': 'object'
                }
            }
        },
        'usage_example': {
            'javascript': '''
// Example: Connect to voice agent
const response = await fetch('http://localhost:8000/api/connect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        room_name: 'my-room',
        user_id: 'user-123',
        user_name: 'John Doe'
    })
});

const data = await response.json();
// Use data.token and data.url to connect with LiveKit client

// Import LiveKit client
import { Room } from 'livekit-client';

const room = new Room();
await room.connect(data.url, data.token);
await room.localParticipant.setMicrophoneEnabled(true);
            ''',
            'python': '''
import requests

# Connect to voice agent
response = requests.post('http://localhost:8000/api/connect', json={
    'room_name': 'my-room',
    'user_id': 'user-123',
    'user_name': 'John Doe'
})

data = response.json()
token = data['token']
url = data['url']

# Use token and url with LiveKit Python SDK
            '''
        }
    }
    
    return jsonify(docs)


# =============================================================================
# Run Server
# =============================================================================

if __name__ == '__main__':
    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        print("ERROR: LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set in .env.local")
        exit(1)
    
    print("=" * 70)
    print("🚀 LiveKit Voice Agent - Unified API")
    print("=" * 70)
    print(f"📡 LiveKit URL: {LIVEKIT_URL}")
    print(f"🌐 API Server: http://localhost:8000")
    print(f"📚 Documentation: http://localhost:8000/api")
    print(f"🏥 Health Check: http://localhost:8000/api/health")
    print("=" * 70)
    print("\n🎯 Main Endpoint:")
    print("   POST http://localhost:8000/api/connect")
    print("   Body: { room_name, user_id, user_name }")
    print("\n💡 Make sure your agent is running:")
    print("   uv run python src/agent.py dev")
    print("=" * 70)
    
    app.run(host='0.0.0.0', port=8000, debug=True)

