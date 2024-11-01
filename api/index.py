import os
import logging
from fastapi import FastAPI, WebSocket
import datetime
import json

from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizer

from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import ChatGPTAgentConfig

from vocode.streaming.client_backend.conversation import ConversationRouter
from vocode.streaming.models.message import BaseMessage

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(docs_url=None)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

langsmith_system_prompt = os.getenv("LANGSMITH_SYSTEM_PROMPT")
system_prompt = os.getenv("SYSTEM_PROMPT")
INITIAL_MESSAGE = os.getenv("INITIAL_MESSAGE", "Hello!")


def get_system_prompt():
    if system_prompt:
        return system_prompt
    return "Have a pleasant conversation about life"


def get_chat_gpt_agent():
    return ChatGPTAgent(
        ChatGPTAgentConfig(
            initial_message=BaseMessage(text=INITIAL_MESSAGE),
            prompt_preamble=get_system_prompt(),
            model_name="gpt-4o-mini",
        )
    )


voice_router = ConversationRouter(
    agent_thunk=get_chat_gpt_agent,
    synthesizer_thunk=lambda output_audio_config: AzureSynthesizer(
        AzureSynthesizerConfig.from_output_audio_config(
            output_audio_config, voice_name="en-US-SteffanNeural"
        )
    ),
    conversation_endpoint="/api/python/conversation",
)

app.include_router(voice_router.get_router())


@app.websocket("/api/ping")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        message = json.loads(data)
        # Check if the message contains a 'ping' key
        if message.get("ping") == "ping":
            # Get the current time in UTC as the server receive time
            serverReceiveTime = datetime.datetime.now(datetime.timezone.utc).timestamp()
            # Get the current time in UTC as the server send time
            # Ideally this would be done right before sending
            serverSendTime = datetime.datetime.now(datetime.timezone.utc).timestamp()
            # Send a JSON response containing the server receive time, server send time,
            # and the client send time received from the frontend
            await websocket.send_json(
                {
                    "serverReceiveTime": serverReceiveTime,
                    "serverSendTime": serverSendTime,
                    "clientSendTime": message.get("clientSendTime"),
                }
            )


@app.get("/api/ping")
async def get_ping():
    """
    This function handles GET requests at the /api/ping endpoint.
    When a GET request is received, it returns a JSON response with a 'pong' message.
    """
    return {"message": "pong"}
