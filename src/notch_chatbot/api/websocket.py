"""WebSocket endpoint for real-time chat streaming."""

import asyncio
import json
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect

from notch_chatbot.api.auth import verify_api_key_websocket
from notch_chatbot.api.errors import ErrorCode
from notch_chatbot.api.models import (
    AssistantChunk,
    AssistantComplete,
    ConnectionAck,
    ErrorMessage,
    PongMessage,
    UserMessage,
)
from notch_chatbot.api.session_manager import SessionManager


class WebSocketHandler:
    """Handles WebSocket connections for chat sessions."""

    def __init__(self):
        # Lock per session to prevent concurrent message processing
        self._session_locks: dict[str, asyncio.Lock] = {}

    def _get_session_lock(self, session_id: str) -> asyncio.Lock:
        """Get or create a lock for a session."""
        if session_id not in self._session_locks:
            self._session_locks[session_id] = asyncio.Lock()
        return self._session_locks[session_id]

    async def handle_connection(
        self, websocket: WebSocket, sessions: SessionManager, agent: Any, kb: Any
    ):
        """
        Handle a WebSocket connection lifecycle.

        Args:
            websocket: The WebSocket connection
            sessions: SessionManager instance
            agent: Pydantic AI agent instance
            kb: Knowledge base dependency
        """
        # Extract headers
        headers = dict(websocket.headers)

        # Validate API key
        if not verify_api_key_websocket(headers):
            await websocket.close(code=1008, reason="Invalid API key")
            return

        # Extract session_id from header
        session_id = headers.get("x-session-id")
        if not session_id:
            await websocket.close(code=1008, reason="Missing X-Session-Id header")
            return

        # Verify session exists
        if not sessions.session_exists(session_id):
            await websocket.close(code=1008, reason="Session not found")
            return

        # Accept connection
        await websocket.accept()

        # Mark session as connected
        sessions.mark_connected(session_id)

        try:
            # Send connection acknowledgment
            ack = ConnectionAck(session_id=session_id)
            await websocket.send_json(ack.model_dump())

            # Enter message loop
            await self._message_loop(websocket, session_id, sessions, agent, kb)

        except WebSocketDisconnect:
            # Normal disconnect
            pass
        except Exception as e:
            # Unexpected error
            print(f"WebSocket error for session {session_id}: {e}")
        finally:
            # Mark session as disconnected
            sessions.mark_disconnected(session_id)

    async def _message_loop(
        self,
        websocket: WebSocket,
        session_id: str,
        sessions: SessionManager,
        agent: Any,
        kb: Any,
    ):
        """
        Main message processing loop.

        Args:
            websocket: The WebSocket connection
            session_id: Session identifier
            sessions: SessionManager instance
            agent: Pydantic AI agent instance
            kb: Knowledge base dependency
        """
        while True:
            # Receive message from client
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
            except json.JSONDecodeError:
                error = ErrorMessage(
                    error_code=ErrorCode.INVALID_MESSAGE.value,
                    message="Invalid JSON format",
                )
                await websocket.send_json(error.model_dump())
                continue
            except Exception:
                # Connection closed or other error
                break

            # Parse message type
            msg_type = message.get("type")

            if msg_type == "ping":
                # Handle ping
                pong = PongMessage()
                await websocket.send_json(pong.model_dump())

            elif msg_type == "user_message":
                # Handle user message
                try:
                    user_msg = UserMessage(**message)
                    await self._handle_user_message(
                        websocket, session_id, user_msg.content, sessions, agent, kb
                    )
                except Exception as e:
                    error = ErrorMessage(
                        error_code=ErrorCode.AGENT_ERROR.value,
                        message=f"Failed to process message: {str(e)}",
                    )
                    await websocket.send_json(error.model_dump())

            else:
                # Unknown message type
                error = ErrorMessage(
                    error_code=ErrorCode.INVALID_MESSAGE.value,
                    message=f"Unknown message type: {msg_type}",
                )
                await websocket.send_json(error.model_dump())

    async def _handle_user_message(
        self,
        websocket: WebSocket,
        session_id: str,
        user_message: str,
        sessions: SessionManager,
        agent: Any,
        kb: Any,
    ):
        """
        Handle a user message and stream agent response.

        Args:
            websocket: The WebSocket connection
            session_id: Session identifier
            user_message: User's message content
            sessions: SessionManager instance
            agent: Pydantic AI agent instance
            kb: Knowledge base dependency
        """
        # Get session lock to prevent concurrent processing
        lock = self._get_session_lock(session_id)
        if lock.locked():
            # Agent is busy processing previous message
            error = ErrorMessage(
                error_code=ErrorCode.AGENT_BUSY.value,
                message="Agent is processing previous message",
            )
            await websocket.send_json(error.model_dump())
            return

        async with lock:
            # Get session history
            session = sessions.get_session(session_id)
            if not session:
                error = ErrorMessage(
                    error_code=ErrorCode.SESSION_NOT_FOUND.value,
                    message="Session not found",
                )
                await websocket.send_json(error.model_dump())
                return

            # Run agent with streaming
            try:
                full_response = ""
                async with agent.run_stream(
                    user_message, deps=kb, message_history=session.message_history
                ) as response:
                    # Stream chunks to client
                    async for chunk in response.stream_text(delta=True):
                        full_response += chunk
                        chunk_msg = AssistantChunk(content=chunk, session_id=session_id)
                        await websocket.send_json(chunk_msg.model_dump())

                    # Send completion message
                    complete_msg = AssistantComplete(
                        content=full_response, session_id=session_id
                    )
                    await websocket.send_json(complete_msg.model_dump())

                    # Update session with new message history
                    sessions.update_session(session_id, response.new_messages())

            except Exception as e:
                error = ErrorMessage(
                    error_code=ErrorCode.AGENT_ERROR.value,
                    message=f"Agent error: {str(e)}",
                )
                await websocket.send_json(error.model_dump())


# Global handler instance
ws_handler = WebSocketHandler()


async def websocket_endpoint(
    websocket: WebSocket,
):
    """
    WebSocket endpoint for chat streaming.

    Headers required:
    - X-API-Key: API authentication key
    - X-Session-Id: Session identifier (from POST /api/sessions)
    """
    # Get app state
    sessions = websocket.app.state.sessions
    agent = websocket.app.state.agent
    kb = websocket.app.state.kb

    await ws_handler.handle_connection(websocket, sessions, agent, kb)
