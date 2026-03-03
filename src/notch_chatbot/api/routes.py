"""REST API endpoints for the Notch Chatbot API."""

# ruff: noqa: B008 - FastAPI Depends() in function defaults is standard pattern

from fastapi import APIRouter, Depends, HTTPException, Request

from notch_chatbot.api.auth import verify_api_key
from notch_chatbot.api.errors import APIError, ErrorCode
from notch_chatbot.api.models import (
    HealthCheckResponse,
    SessionCreateRequest,
    SessionCreateResponse,
    SessionHistoryResponse,
)
from notch_chatbot.api.session_manager import SessionManager

router = APIRouter()


def get_session_manager(request: Request) -> SessionManager:
    """Dependency to get SessionManager from app state."""
    return request.app.state.sessions


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(request: Request):
    """
    Health check endpoint (no authentication required).

    Returns server status and initialization state.
    """
    app_state = request.app.state
    return HealthCheckResponse(
        status="healthy",
        version="0.1.0",
        knowledge_base_loaded=hasattr(app_state, "kb") and app_state.kb is not None,
        agent_initialized=hasattr(app_state, "agent") and app_state.agent is not None,
    )


@router.post(
    "/sessions",
    response_model=SessionCreateResponse,
    dependencies=[Depends(verify_api_key)],
)
async def create_session(
    request_body: SessionCreateRequest,
    sessions: SessionManager = Depends(get_session_manager),
):
    """
    Create a new conversation session.

    Requires:
    - X-API-Key header for authentication
    - session_id in request body (client-generated)

    Returns:
    - 200: Session created successfully
    - 400: session_id missing or already exists
    - 401: Invalid API key
    """
    session_id = request_body.session_id

    # Validate session_id is provided
    if not session_id:
        raise APIError(
            error_code=ErrorCode.SESSION_ID_REQUIRED,
            message="session_id is required in request body",
            status_code=400,
        )

    # Try to create session
    created = sessions.create_session(session_id)
    if not created:
        raise APIError(
            error_code=ErrorCode.SESSION_ALREADY_EXISTS,
            message=f"Session ID '{session_id}' already exists",
            status_code=400,
        )

    # Get the created session
    session = sessions.get_session(session_id)
    return SessionCreateResponse(
        session_id=session.session_id,
        created_at=session.created_at,
        expires_in_minutes=30,
    )


@router.get(
    "/sessions/{session_id}/history",
    response_model=SessionHistoryResponse,
    dependencies=[Depends(verify_api_key)],
)
async def get_session_history(
    session_id: str,
    sessions: SessionManager = Depends(get_session_manager),
):
    """
    Get conversation history for a session.

    Requires:
    - X-API-Key header for authentication

    Returns:
    - 200: Session history
    - 404: Session not found
    - 401: Invalid API key
    """
    session = sessions.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Convert message history to simple format for client
    messages = []
    for msg in session.message_history:
        if hasattr(msg, "model_dump"):
            messages.append(msg.model_dump())
        else:
            messages.append({"content": str(msg)})

    return SessionHistoryResponse(
        session_id=session_id, messages=messages, message_count=len(messages)
    )


@router.delete(
    "/sessions/{session_id}",
    dependencies=[Depends(verify_api_key)],
)
async def delete_session(
    session_id: str,
    sessions: SessionManager = Depends(get_session_manager),
):
    """
    Delete a conversation session.

    Requires:
    - X-API-Key header for authentication

    Returns:
    - 200: Session deleted successfully
    - 404: Session not found
    - 401: Invalid API key
    """
    deleted = sessions.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"message": "Session deleted successfully", "session_id": session_id}
