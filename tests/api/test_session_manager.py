"""Tests for SessionManager."""

from datetime import datetime, timedelta

import pytest

from notch_chatbot.api.session_manager import SessionManager


def test_create_session():
    """Test session creation."""
    manager = SessionManager()
    session_id = "test-session-123"

    # Create session
    created = manager.create_session(session_id)
    assert created is True

    # Verify session exists
    assert manager.session_exists(session_id)

    # Try creating same session again - should fail
    created_again = manager.create_session(session_id)
    assert created_again is False


def test_get_session():
    """Test getting a session."""
    manager = SessionManager()
    session_id = "test-session-456"

    # Get non-existent session
    session = manager.get_session(session_id)
    assert session is None

    # Create and get session
    manager.create_session(session_id)
    session = manager.get_session(session_id)
    assert session is not None
    assert session.session_id == session_id
    assert session.message_history == []
    assert session.ws_connected is False


def test_mark_connected_disconnected():
    """Test marking session as connected/disconnected."""
    manager = SessionManager()
    session_id = "test-session-789"

    manager.create_session(session_id)
    session = manager.get_session(session_id)
    assert session.ws_connected is False

    # Mark connected
    manager.mark_connected(session_id)
    session = manager.get_session(session_id)
    assert session.ws_connected is True

    # Mark disconnected
    manager.mark_disconnected(session_id)
    session = manager.get_session(session_id)
    assert session.ws_connected is False


def test_update_session():
    """Test updating session message history."""
    manager = SessionManager()
    session_id = "test-session-update"

    manager.create_session(session_id)

    # Update with messages
    new_messages = [{"role": "user", "content": "Hello"}]
    manager.update_session(session_id, new_messages)

    session = manager.get_session(session_id)
    assert session.message_history == new_messages


def test_delete_session():
    """Test deleting a session."""
    manager = SessionManager()
    session_id = "test-session-delete"

    # Delete non-existent session
    deleted = manager.delete_session(session_id)
    assert deleted is False

    # Create and delete session
    manager.create_session(session_id)
    assert manager.session_exists(session_id)

    deleted = manager.delete_session(session_id)
    assert deleted is True
    assert not manager.session_exists(session_id)


@pytest.mark.asyncio
async def test_cleanup_expired():
    """Test cleanup of expired sessions."""
    manager = SessionManager(ttl_minutes=1)  # 1 minute TTL

    # Create sessions
    session1 = "session-1"
    session2 = "session-2"
    manager.create_session(session1)
    manager.create_session(session2)

    # Manually set session1 to be expired
    session = manager.get_session(session1)
    session.last_activity = datetime.now() - timedelta(minutes=2)

    # Run cleanup
    removed = await manager.cleanup_expired()
    assert removed == 1
    assert not manager.session_exists(session1)
    assert manager.session_exists(session2)


def test_get_session_count():
    """Test getting session count."""
    manager = SessionManager()

    assert manager.get_session_count() == 0

    manager.create_session("session-1")
    manager.create_session("session-2")
    assert manager.get_session_count() == 2

    manager.delete_session("session-1")
    assert manager.get_session_count() == 1
