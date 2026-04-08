"""Pydantic models for API request and response schemas."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel


# REST API Models
class SessionCreateRequest(BaseModel):
    """Request to create a new session."""

    session_id: str


class SessionCreateResponse(BaseModel):
    """Response after creating a session."""

    session_id: str
    created_at: datetime
    expires_in_minutes: int = 30


class SessionHistoryResponse(BaseModel):
    """Response containing conversation history."""

    session_id: str
    messages: list[dict[str, Any]]
    message_count: int


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    knowledge_base_loaded: bool
    agent_initialized: bool


# WebSocket Message Models (Client → Server)
class UserMessage(BaseModel):
    """User sends a chat message."""

    type: Literal["user_message"] = "user_message"
    content: str


class PingMessage(BaseModel):
    """Keepalive ping from client."""

    type: Literal["ping"] = "ping"


# WebSocket Message Models (Server → Client)
class ConnectionAck(BaseModel):
    """Connection acknowledgment."""

    type: Literal["connection_ack"] = "connection_ack"
    session_id: str


class AssistantChunk(BaseModel):
    """Streaming text chunk from assistant."""

    type: Literal["assistant_chunk"] = "assistant_chunk"
    content: str
    session_id: str


class AssistantComplete(BaseModel):
    """Response complete message."""

    type: Literal["assistant_complete"] = "assistant_complete"
    content: str
    session_id: str


class ErrorMessage(BaseModel):
    """Error message."""

    type: Literal["error"] = "error"
    error_code: str
    message: str


class PongMessage(BaseModel):
    """Keepalive pong response."""

    type: Literal["pong"] = "pong"


# Send Offer Models
class SendOfferRequest(BaseModel):
    """Request to generate and send a proposal PDF by email."""

    client_name: str
    client_email: str
    project_description: str
    services_list: str
    project_scope: str = "medium"


class SendOfferResponse(BaseModel):
    """Response after sending a proposal."""

    success: bool
    message: str
