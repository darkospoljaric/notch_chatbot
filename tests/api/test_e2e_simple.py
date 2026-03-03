"""Simple end-to-end test using TestClient."""

import os
import uuid

import pytest
from fastapi.testclient import TestClient

from notch_chatbot.api.app import app


@pytest.fixture
def client():
    """Create test client with initialized app state."""
    os.environ["API_KEY"] = "test-key-e2e"
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "test-key")
    os.environ["SENDGRID_API_KEY"] = os.getenv("SENDGRID_API_KEY", "test-key")

    with TestClient(app) as test_client:
        yield test_client


def test_end_to_end_session_flow(client):
    """Test complete session creation and management flow."""
    api_key = "test-key-e2e"
    session_id = str(uuid.uuid4())

    # 1. Health check
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["knowledge_base_loaded"] is True
    print("✓ Health check passed")

    # 2. Create session
    response = client.post(
        "/api/sessions",
        headers={"X-API-Key": api_key},
        json={"session_id": session_id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    print(f"✓ Session created: {session_id}")

    # 3. Try creating duplicate session - should fail
    response = client.post(
        "/api/sessions",
        headers={"X-API-Key": api_key},
        json={"session_id": session_id},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "SESSION_ALREADY_EXISTS"
    print("✓ Duplicate session rejected")

    # 4. Get session history (should be empty)
    response = client.get(
        f"/api/sessions/{session_id}/history", headers={"X-API-Key": api_key}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message_count"] == 0
    print("✓ Session history retrieved (empty)")

    # 5. Delete session
    response = client.delete(
        f"/api/sessions/{session_id}", headers={"X-API-Key": api_key}
    )
    assert response.status_code == 200
    print("✓ Session deleted")

    # 6. Verify session is gone
    response = client.get(
        f"/api/sessions/{session_id}/history", headers={"X-API-Key": api_key}
    )
    assert response.status_code == 404
    print("✓ Session no longer exists")

    print("\n✅ End-to-end test passed!")


def test_api_key_validation(client):
    """Test API key validation across endpoints."""
    session_id = str(uuid.uuid4())

    # Test with wrong API key
    response = client.post(
        "/api/sessions",
        headers={"X-API-Key": "wrong-key"},
        json={"session_id": session_id},
    )
    assert response.status_code == 401
    print("✓ Invalid API key rejected")

    # Test with missing API key
    response = client.post("/api/sessions", json={"session_id": session_id})
    assert response.status_code == 422  # Validation error
    print("✓ Missing API key rejected")

    print("\n✅ API key validation test passed!")
