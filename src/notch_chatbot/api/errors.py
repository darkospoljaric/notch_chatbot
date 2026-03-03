"""Error codes and exception handling for the Notch Chatbot API."""

from enum import Enum

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class ErrorCode(str, Enum):
    """Error codes for API responses."""

    INVALID_API_KEY = "INVALID_API_KEY"
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    SESSION_ALREADY_EXISTS = "SESSION_ALREADY_EXISTS"
    SESSION_ID_REQUIRED = "SESSION_ID_REQUIRED"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    AGENT_ERROR = "AGENT_ERROR"
    INVALID_MESSAGE = "INVALID_MESSAGE"
    AGENT_BUSY = "AGENT_BUSY"


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, error_code: ErrorCode, message: str, status_code: int = 400):
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle APIError exceptions and return formatted JSON response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": exc.error_code.value, "message": exc.message},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException and return formatted JSON response."""
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
