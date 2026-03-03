"""Tests for REST API endpoints."""

import os

import pytest
from fastapi.testclient import TestClient

from notch_chatbot.api.app import app


@pytest.fixture
def client():
    """Create test client with initialized app state."""
    os.environ["API_KEY"] = "test-key-123"
    os.environ["SENDGRID_API_KEY"] = "test-sendgrid-key"

    # Use TestClient with lifespan events
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert data["knowledge_base_loaded"] is True
    assert data["agent_initialized"] is True


def test_create_session_success(client):
    """Test successful session creation."""
    response = client.post(
        "/api/sessions",
        headers={"X-API-Key": "test-key-123"},
        json={"session_id": "test-session-001"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test-session-001"
    assert "created_at" in data
    assert data["expires_in_minutes"] == 30


def test_create_session_missing_api_key(client):
    """Test session creation without API key."""
    response = client.post("/api/sessions", json={"session_id": "test-session-002"})
    assert response.status_code == 422  # FastAPI validation error for missing header


def test_create_session_invalid_api_key(client):
    """Test session creation with invalid API key."""
    response = client.post(
        "/api/sessions",
        headers={"X-API-Key": "wrong-key"},
        json={"session_id": "test-session-003"},
    )
    assert response.status_code == 401


def test_create_session_missing_session_id(client):
    """Test session creation without session_id in body."""
    response = client.post("/api/sessions", headers={"X-API-Key": "test-key-123"})
    assert response.status_code == 422  # Validation error


def test_create_session_duplicate(client):
    """Test creating duplicate session."""
    session_id = "test-session-duplicate"

    # Create first session
    response1 = client.post(
        "/api/sessions",
        headers={"X-API-Key": "test-key-123"},
        json={"session_id": session_id},
    )
    assert response1.status_code == 200

    # Try to create same session again
    response2 = client.post(
        "/api/sessions",
        headers={"X-API-Key": "test-key-123"},
        json={"session_id": session_id},
    )
    assert response2.status_code == 400
    data = response2.json()
    assert data["error_code"] == "SESSION_ALREADY_EXISTS"


def test_get_session_history(client):
    """Test getting session history."""
    session_id = "test-session-history"

    # Create session
    client.post(
        "/api/sessions",
        headers={"X-API-Key": "test-key-123"},
        json={"session_id": session_id},
    )

    # Get history
    response = client.get(
        f"/api/sessions/{session_id}/history", headers={"X-API-Key": "test-key-123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert data["messages"] == []
    assert data["message_count"] == 0


def test_get_session_history_not_found(client):
    """Test getting history for non-existent session."""
    response = client.get(
        "/api/sessions/non-existent/history", headers={"X-API-Key": "test-key-123"}
    )
    assert response.status_code == 404


def test_delete_session(client):
    """Test deleting a session."""
    session_id = "test-session-delete"

    # Create session
    client.post(
        "/api/sessions",
        headers={"X-API-Key": "test-key-123"},
        json={"session_id": session_id},
    )

    # Delete session
    response = client.delete(
        f"/api/sessions/{session_id}", headers={"X-API-Key": "test-key-123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id

    # Verify session is gone
    response = client.get(
        f"/api/sessions/{session_id}/history", headers={"X-API-Key": "test-key-123"}
    )
    assert response.status_code == 404


def test_delete_session_not_found(client):
    """Test deleting non-existent session."""
    response = client.delete(
        "/api/sessions/non-existent", headers={"X-API-Key": "test-key-123"}
    )
    assert response.status_code == 404
