"""Tests for API key authentication."""

import os

from notch_chatbot.api.auth import verify_api_key_websocket


def test_verify_api_key_websocket_valid():
    """Test WebSocket API key verification with valid key."""
    os.environ["API_KEY"] = "test-key-123"

    headers = {"x-api-key": "test-key-123"}
    result = verify_api_key_websocket(headers)
    assert result is True


def test_verify_api_key_websocket_invalid():
    """Test WebSocket API key verification with invalid key."""
    os.environ["API_KEY"] = "test-key-123"

    headers = {"x-api-key": "wrong-key"}
    result = verify_api_key_websocket(headers)
    assert result is False


def test_verify_api_key_websocket_missing():
    """Test WebSocket API key verification with missing key."""
    os.environ["API_KEY"] = "test-key-123"

    headers = {}
    result = verify_api_key_websocket(headers)
    assert result is False


def test_verify_api_key_websocket_no_env():
    """Test WebSocket API key verification when API_KEY not set."""
    if "API_KEY" in os.environ:
        del os.environ["API_KEY"]

    headers = {"x-api-key": "any-key"}
    result = verify_api_key_websocket(headers)
    assert result is False
