"""Simple token server for testing the voice agent."""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from livekit import api
from dotenv import load_dotenv

load_dotenv(".env.local")

app = Flask(__name__)
CORS(app)  # Enable CORS for local testing

# Get LiveKit credentials from environment
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

@app.route('/token', methods=['GET', 'POST'])
def generate_token():
    """Generate a LiveKit access token."""
    try:
        # Get parameters from request
        if request.method == 'GET':
            room_name = request.args.get('room', f'test-room-{int(os.times().elapsed)}')
            identity = request.args.get('identity', 'web-user')
        else:
            data = request.json or {}
            room_name = data.get('room', f'test-room-{int(os.times().elapsed)}')
            identity = data.get('identity', 'web-user')

        # Create access token
        token = api.AccessToken(LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
        token.with_identity(identity)
        token.with_name(identity)
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

        return jsonify({
            'token': jwt_token,
            'url': os.getenv('LIVEKIT_URL'),
            'room': room_name
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    if not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        print("ERROR: LIVEKIT_API_KEY and LIVEKIT_API_SECRET must be set in .env.local")
        exit(1)
    
    print("=" * 60)
    print("Token Server Starting")
    print("=" * 60)
    print(f"LiveKit URL: {os.getenv('LIVEKIT_URL')}")
    print(f"Server running on: http://localhost:5000")
    print(f"Token endpoint: http://localhost:5000/token")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

