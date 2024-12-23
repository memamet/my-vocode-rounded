import os
import logging
from fastapi import FastAPI, WebSocket, Query
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import datetime
import json

from pydantic import BaseModel
from vocode.streaming.models.synthesizer import AzureSynthesizerConfig
from vocode.streaming.synthesizer.azure_synthesizer import AzureSynthesizer

from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import ChatGPTAgentConfig

from vocode.streaming.client_backend.conversation import ConversationRouter
from vocode.streaming.models.message import BaseMessage

from openai import OpenAI
from utils.prompt import ClientMessage, convert_to_openai_messages

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://my-vocode-rounded.vercel.app"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

langsmith_system_prompt = os.getenv("LANGSMITH_SYSTEM_PROMPT")
system_prompt = os.getenv("SYSTEM_PROMPT")
INITIAL_MESSAGE = os.getenv("INITIAL_MESSAGE", "Hello!")


class Request(BaseModel):
    messages: list[ClientMessage]


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


def stream_text(messages: list[ClientMessage], protocol: str = "data"):

    messages.insert(0, {"role": "system", "content": get_system_prompt()})

    stream = client.chat.completions.create(
        messages=messages,
        model="gpt-4o-mini",
        stream=True,
    )

    for chunk in stream:
        for choice in chunk.choices:
            if choice.finish_reason == "stop":
                break
            else:
                yield "{text}".format(text=choice.delta.content)


@app.post("/api/chat")
async def handle_chat_data(request: Request, protocol: str = Query("data")):
    messages = request.messages
    openai_messages = convert_to_openai_messages(messages)

    response = StreamingResponse(stream_text(openai_messages, protocol))
    response.headers["x-vercel-ai-data-stream"] = "v1"
    return response


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



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 if PORT is not set
    uvicorn.run(app, host="0.0.0.0", port=port)