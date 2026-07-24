from fastapi import FastAPI, HTTPException

from backend.api.schemas import ChatRequest, ChatResponse, SessionResponse
from backend.services.agent_runner import create_session, run_turn, session_exists

app = FastAPI(title="Travel Agent MVP")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/sessions", response_model=SessionResponse)
async def new_session():
    session_id = await create_session()
    return SessionResponse(session_id=session_id)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
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
