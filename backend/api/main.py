"""Thin HTTP interface over the agent system.

Routes only handle HTTP concerns (parse request, call agent_runner, shape
the response/error) — no agent or session business logic lives here, per
plan.md Step 8.
"""

from fastapi import FastAPI, HTTPException

from backend.api.schemas import ChatRequest, ChatResponse, SessionResponse
from backend.services.agent_runner import create_session, run_turn, session_exists

app = FastAPI(title="Travel Agent MVP")

@app.get("/health")
async def health():
    """Liveness check: is the server process up and reachable."""
    return {"status": "ok"}

@app.post("/sessions", response_model=SessionResponse)
async def new_session():
    """Creates a new, empty conversation and returns its session_id.

    Call this once per conversation; reuse the returned session_id on every
    subsequent /chat call to keep the context together.
    """
    session_id = await create_session()
    return SessionResponse(session_id=session_id)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Sends one message to an existing session and returns the reply.

    404 if session_id wasn't created via /sessions first; 502 if the
    upstream model/agent call itself fails (e.g. quota errors).
    """
    if not await session_exists(request.session_id):
        raise HTTPException(
            status_code=404,
            detail="Session not found. Create on via POST /sessions first."
        )
    try:
        reply = await run_turn(request.session_id, request.message)
    except Exception as e:
        # 502: the API itself is fine, but the upstream agent/model call failed
        # (e.g. the quota errors you hit earlier) — distinct from a 500 bug in our own code.
        raise HTTPException(status_code=502, detail=f"Agent failed to respond: {e}")

    return ChatResponse(session_id=request.session_id, response=reply)
