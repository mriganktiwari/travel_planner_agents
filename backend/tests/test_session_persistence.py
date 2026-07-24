"""Zero-LLM-cost check that DatabaseSessionService actually persists to
disk: run once to create a session, run again to confirm it's found."""

import asyncio
from google.adk.sessions import DatabaseSessionService

APP_NAME = "persistence_check"
USER_ID = "test_user"
SESSION_ID = "persistence_check_session"

session_service = DatabaseSessionService(
    db_url="sqlite+aiosqlite:///data/travel_agent.db"
)

async def main():
    existing = await session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    if existing:
        print(f"Found existing session. events={len(existing.events)}, state={existing.state}")
    else:
        print("No existing session — creating one.")
        await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID,
            state={"created_by": "run 1"},
        )

if __name__ == "__main__":
    asyncio.run(main())
