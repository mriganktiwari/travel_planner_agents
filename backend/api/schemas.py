"""Request/response contracts for the API — the concrete data shapes that
implement docs/product-contract.md at the HTTP layer."""

from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Body for POST /chat."""
    session_id: str
    message: str

class ChatResponse(BaseModel):
    """Body returned by POST /chat."""
    session_id: str
    response: str
    status: str = "ok"

class SessionResponse(BaseModel):
    """Body returned by POST /sessions."""
    session_id: str
