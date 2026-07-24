"""Standalone test for destination_agent, run in isolation (no root_agent)."""

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from backend.travel_agent.destinations_agent import destination_agent

session_service = InMemorySessionService()
# later we persist this conversation state in SQLite

APP_NAME = 'destination_agent_test'
USER_ID = 'test_user'
SESSION_ID = 'destination_agent_test_session'

async def main():
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=destination_agent, app_name=APP_NAME, session_service=session_service
    )

    user_message = types.Content(
        role='user',
        parts=[types.Part(text='i want to plan a trip to koh lipe & koh lanta for 7-8 days in december. what are your suggestions, are both similar so only 1 should be better?')],
    )

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
