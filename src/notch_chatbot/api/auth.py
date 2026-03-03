"""API key authentication for the Notch Chatbot API."""

import os

from fastapi import Header, HTTPException


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """
    Verify API key from X-API-Key header.

    Args:
        x_api_key: API key from request header

    Returns:
        The validated API key

    Raises:
        HTTPException: 401 if API key is invalid or missing
    """
    expected_key = os.getenv("API_KEY")
    if not expected_key:
        raise HTTPException(status_code=500, detail="API_KEY not configured on server")
    if x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


def verify_api_key_websocket(headers: dict) -> bool:
    """
    Verify API key from WebSocket headers.

    Args:
        headers: WebSocket headers dictionary

    Returns:
        True if API key is valid, False otherwise
    """
    api_key = headers.get("x-api-key")
    expected_key = os.getenv("API_KEY")
    if not api_key or not expected_key or api_key != expected_key:
        return False
    return True
