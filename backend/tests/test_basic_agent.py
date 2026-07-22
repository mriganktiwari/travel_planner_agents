from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import asyncio
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

root_agent = Agent(
    name='test_travel_agent',
    model='gemini-2.5-flash',
    description="Basic travel assistant for testing ADK + Gemini connectivity.",
    instruction="You are a helpful travel assistant. Answer briefly.",
)

session_service = InMemorySessionService()
# later we persist this conversation state in SQLite

APP_NAME = 'trave_agent_mvp'
USER_ID = 'test_user'
SESSION_ID = 'test_session'

async def main():
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )

    user_message = types.Content(
        role='user',
        parts=[types.Part(text='Suggest five weekend destination near Satna.')],
    )

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
