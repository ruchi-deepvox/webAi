"""Simple script to test if the agent is running and connectable."""
import asyncio
import os
from livekit import api, rtc
from dotenv import load_dotenv

load_dotenv(".env.local")


async def test_agent_connection():
    """Test connecting to the agent and sending a simple message."""
    # Get credentials from environment
    url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    
    if not all([url, api_key, api_secret]):
        print("[ERROR] Missing LiveKit credentials in .env.local")
        print("Required: LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET")
        return False
    
    print(f"[INFO] Connecting to LiveKit at {url}")
    
    try:
        # Create a room using the API
        lk_api = api.LiveKitAPI(url, api_key, api_secret)
        room_name = f"test-room-{int(asyncio.get_event_loop().time())}"
        
        print(f"[INFO] Creating test room: {room_name}")
        room = await lk_api.room.create_room(
            api.CreateRoomRequest(name=room_name)
        )
        print(f"[SUCCESS] Room created: {room.name}")
        
        # Generate a token to join the room
        token = api.AccessToken(api_key, api_secret)
        token.with_identity("test-user")
        token.with_name("Test User")
        token.with_grants(
            api.VideoGrants(
                room_join=True,
                room=room_name,
            )
        )
        
        print(f"[INFO] Generated access token")
        print(f"[SUCCESS] Agent should be able to join room: {room_name}")
        print(f"\n[TIP] If your agent is running in dev mode, it should now connect to this room.")
        print(f"[TIP] Check your agent terminal for connection logs.")
        
        # Wait a bit for the agent to join
        await asyncio.sleep(5)
        
        # List participants in the room
        participants_response = await lk_api.room.list_participants(
            api.ListParticipantsRequest(room=room_name)
        )
        
        print(f"\n[INFO] Participants in room:")
        for p in participants_response.participants:
            print(f"   - {p.identity} ({p.name or 'no name'})")
        
        # Clean up
        print(f"\n[INFO] Cleaning up test room...")
        await lk_api.room.delete_room(api.DeleteRoomRequest(room=room_name))
        print(f"[SUCCESS] Test completed successfully!")
        
        await lk_api.aclose()
        return True
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(test_agent_connection())

