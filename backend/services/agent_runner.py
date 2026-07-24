import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from backend.travel_agent.root_agent import root_agent

load_dotenv()

APP_NAME = 'travel_agent_mvp'
USER_ID = 'anonymous' # as not auth in this MVP

session_service = DatabaseSessionService(
    db_url = "sqlite+aiosqlite:///data/travel_agent.db"
)

runner = Runner(
    agent=root_agent, app_name=APP_NAME, session_service=session_service
)


async def create_session() -> str:
    """Creates a new, empty session and returns its ID."""
    session_id = str(uuid.uuid4())
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    return session_id


async def session_exists(session_id: str) -> bool:
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    return session is not None


async def run_turn(session_id: str, message: str) -> str:
    """Sends one user message to root_agent and returns its final text reply."""
    user_message = types.Content(role='user', parts=[types.Part(text=message)])
    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session_id, new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text
    return final_text
