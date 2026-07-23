import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService
from google.adk.sessions import DatabaseSessionService
from google.genai import types
import asyncio
from dotenv import load_dotenv

from backend.travel_agent.root_agent import root_agent

load_dotenv()

# session_service = InMemorySessionService()
session_service = DatabaseSessionService(
    db_url="sqlite+aiosqlite:///data/travel_agent.db"
)

APP_NAME = "root_agent_test"
USER_ID = "test_user"
SESSION_ID = "root_agent_test_session"

async def print_session_state(label):
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    print(f"\n[{label}] state: {session.state}")
    print(f"[{label}] event count: {len(session.events)}")

async def send(runner, text):
    user_message = types.Content(role="user", parts=[types.Part(text=text)])
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)

async def get_or_create_session():
    existing = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if existing:
        print(f"Resuming session with {len(existing.events)} prior events.")
        return existing
    print("Creating new session.")
    return await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

async def main():
    await get_or_create_session()
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

    # print("--- Turn 1 ---")
    # await send(runner, "Plan a five-day Leh-Ladakh trip for a family of four.")

    print("--- Turn 2 (follow-up) ---")
    await send(runner, "The 5 days specified should exclude  arrival and departure days.")


    # print("--- Turn 1 ---")
    # await print_session_state("before turn 1")
    # await send(runner, "Plan a 10-day Thailand trip for a family of 3.")
    # await print_session_state("after turn 1")

    # print("--- Turn 2 (follow-up) ---")
    # await print_session_state("before turn 2")
    # await send(runner, "Make day three less tiring and reduce expensive activities.")
    # await print_session_state("after turn 2")


if __name__ == "__main__":
    asyncio.run(main())
