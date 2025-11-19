import logging
import json

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    inference,
    room_io,
)
from livekit.plugins import noise_cancellation, silero, elevenlabs
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self, custom_instructions: str = None) -> None:
        # Default instructions
        default_instructions = """You are a helpful voice AI assistant. The user is interacting with you via voice, even if you perceive the conversation as text.
            You eagerly assist users with their questions by providing information from your extensive knowledge.
            Your responses are concise, to the point, and without any complex formatting or punctuation including emojis, asterisks, or other symbols.
            You are curious, friendly, and have a sense of humor."""
        
        # Use custom instructions if provided, otherwise use default
        instructions = custom_instructions if custom_instructions else default_instructions
        
        super().__init__(
            instructions=instructions,
        )
        
        logger.info(f"Agent initialized with {'custom' if custom_instructions else 'default'} instructions")

    # To add tools, use the @function_tool decorator.
    # Here's an example that adds a simple weather tool.
    # You also have to add `from livekit.agents import function_tool, RunContext` to the top of this file
    # @function_tool
    # async def lookup_weather(self, context: RunContext, location: str):
    #     """Use this tool to look up current weather information in the given location.
    #
    #     If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.
    #
    #     Args:
    #         location: The location to look up weather information for (e.g. city name)
    #     """
    #
    #     logger.info(f"Looking up weather for {location}")
    #
    #     return "sunny with a temperature of 70 degrees."


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session()
async def my_agent(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }
    
    # Check for custom configuration from participants
    custom_instructions = None
    tts_provider = "cartesia"  # Default
    voice_id = None
    
    # Wait a bit for participants to join and then check their metadata
    await ctx.connect()
    
    # Check all participants for custom configuration
    for participant in ctx.room.remote_participants.values():
        if participant.metadata:
            try:
                metadata = json.loads(participant.metadata)
                if 'instructions' in metadata:
                    custom_instructions = metadata['instructions']
                    logger.info(f"Using custom instructions from participant {participant.identity}")
                if 'tts_provider' in metadata:
                    tts_provider = metadata['tts_provider']
                    logger.info(f"Using TTS provider: {tts_provider}")
                if 'voice_id' in metadata:
                    voice_id = metadata['voice_id']
                    logger.info(f"Using voice ID: {voice_id}")
                break
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse metadata for participant {participant.identity}")

    # Configure TTS based on provider
    if tts_provider.lower() == "elevenlabs":
        # ElevenLabs TTS - Use dedicated plugin
        default_voice = "0p0kYzKW1Gq5uoKh8Qod"  # User's preferred ElevenLabs voice
        selected_voice = voice_id if voice_id else default_voice
        tts_config = elevenlabs.TTS(voice=selected_voice)
        logger.info(f"Configured ElevenLabs TTS with voice: {selected_voice}")
    else:
        # Cartesia TTS (default)
        default_voice = "9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"  # Cartesia Sonic voice
        selected_voice = voice_id if voice_id else default_voice
        tts_config = inference.TTS(
            model="cartesia/sonic-3",
            voice=selected_voice
        )
        logger.info(f"Configured Cartesia TTS with voice: {selected_voice}")
    
    # Set up a voice AI pipeline using OpenAI, selected TTS, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=inference.STT(model="assemblyai/universal-streaming", language="en"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=inference.LLM(model="openai/gpt-4.1-mini"),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=tts_config,
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(custom_instructions=custom_instructions),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: noise_cancellation.BVCTelephony()
                if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                else noise_cancellation.BVC(),
            ),
        ),
    )


if __name__ == "__main__":
    cli.run_app(server)
