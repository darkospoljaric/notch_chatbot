"""Session management for the Notch Chatbot API."""

import asyncio
from datetime import datetime, timedelta
from typing import Any

from pydantic import BaseModel


class ConversationSession(BaseModel):
    """Represents a conversation session."""

    session_id: str
    message_history: list[Any] = []  # Pydantic AI's ModelMessage format
    created_at: datetime
    last_activity: datetime
    ws_connected: bool = False
    metadata: dict[str, Any] = {}


class SessionManager:
    """Manages conversation sessions in memory."""

    def __init__(self, ttl_minutes: int = 30):
        """
        Initialize session manager.

        Args:
            ttl_minutes: Time-to-live for inactive sessions in minutes
        """
        self._sessions: dict[str, ConversationSession] = {}
        self._ttl_minutes = ttl_minutes
        self._cleanup_task: asyncio.Task | None = None
        self._lock = asyncio.Lock()

    def create_session(self, session_id: str) -> bool:
        """
        Create a new session with the provided session ID.

        Args:
            session_id: Client-provided session identifier

        Returns:
            True if session was created, False if session_id already exists
        """
        if session_id in self._sessions:
            return False

        now = datetime.now()
        self._sessions[session_id] = ConversationSession(
            session_id=session_id,
            message_history=[],
            created_at=now,
            last_activity=now,
            ws_connected=False,
            metadata={},
        )
        return True

    def get_session(self, session_id: str) -> ConversationSession | None:
        """
        Retrieve a session by ID.

        Args:
            session_id: Session identifier

        Returns:
            ConversationSession if found, None otherwise
        """
        return self._sessions.get(session_id)

    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: Session identifier

        Returns:
            True if session exists, False otherwise
        """
        return session_id in self._sessions

    def update_session(self, session_id: str, new_messages: list[Any]) -> None:
        """
        Update session with new messages after agent response.

        Args:
            session_id: Session identifier
            new_messages: Updated message history from agent
        """
        session = self._sessions.get(session_id)
        if session:
            session.message_history = new_messages
            session.last_activity = datetime.now()

    def mark_connected(self, session_id: str) -> None:
        """
        Mark session as WebSocket connected.

        Args:
            session_id: Session identifier
        """
        session = self._sessions.get(session_id)
        if session:
            session.ws_connected = True
            session.last_activity = datetime.now()

    def mark_disconnected(self, session_id: str) -> None:
        """
        Mark session as WebSocket disconnected.

        Args:
            session_id: Session identifier
        """
        session = self._sessions.get(session_id)
        if session:
            session.ws_connected = False
            session.last_activity = datetime.now()

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.

        Args:
            session_id: Session identifier

        Returns:
            True if session was deleted, False if not found
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False

    async def cleanup_expired(self) -> int:
        """
        Remove expired sessions based on TTL.

        Returns:
            Number of sessions removed
        """
        async with self._lock:
            now = datetime.now()
            expired_threshold = now - timedelta(minutes=self._ttl_minutes)
            expired_sessions = [
                session_id
                for session_id, session in self._sessions.items()
                if session.last_activity < expired_threshold
            ]

            for session_id in expired_sessions:
                del self._sessions[session_id]

            return len(expired_sessions)

    async def start_cleanup_task(self) -> None:
        """Start background task to clean up expired sessions every 5 minutes."""
        if self._cleanup_task is not None:
            return

        async def cleanup_loop():
            while True:
                await asyncio.sleep(300)  # 5 minutes
                removed = await self.cleanup_expired()
                if removed > 0:
                    print(f"Cleaned up {removed} expired sessions")

        self._cleanup_task = asyncio.create_task(cleanup_loop())

    async def stop_cleanup_task(self) -> None:
        """Stop the background cleanup task."""
        if self._cleanup_task is not None:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None

    def get_session_count(self) -> int:
        """Get total number of active sessions."""
        return len(self._sessions)
