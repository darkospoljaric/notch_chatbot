"""FastAPI application for Notch Chatbot API."""

import json
import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_ai.ag_ui import handle_ag_ui_request
from starlette.requests import Request as StarletteRequest

from notch_chatbot.adapters.email_adapter import EmailServiceAdapter
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base
from notch_chatbot.models import AgentDeps
from notch_chatbot.services.email_strategy import SendGridEmailService

from .errors import APIError, api_error_handler, http_exception_handler
from .routes import router
from .session_manager import SessionManager
from .websocket import websocket_endpoint

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown.

    Loads knowledge base, creates agent, and initializes services.
    """
    print("Starting Notch Chatbot API...")

    # Load knowledge base
    try:
        app.state.kb = load_knowledge_base()
        print(f"✓ Knowledge base loaded: {len(app.state.kb.services)} services")
    except Exception as e:
        print(f"✗ Failed to load knowledge base: {e}")
        raise

    # Initialize email service
    sendgrid_key = os.getenv("SENDGRID_API_KEY")
    if sendgrid_key:
        email_service = SendGridEmailService(sendgrid_key)
        app.state.email_adapter = EmailServiceAdapter(email_service)
        print("✓ Email service initialized")
    else:
        print("⚠ SENDGRID_API_KEY not set - email features disabled")
        # Create a dummy adapter for development
        email_service = SendGridEmailService("")
        app.state.email_adapter = EmailServiceAdapter(email_service)

    # Create agent
    try:
        app.state.agent = create_notch_agent(app.state.email_adapter)
        print("✓ AI agent initialized")
    except Exception as e:
        print(f"✗ Failed to create agent: {e}")
        raise

    # Initialize session manager
    app.state.sessions = SessionManager(ttl_minutes=30)
    await app.state.sessions.start_cleanup_task()
    print("✓ Session manager initialized")

    print("🚀 Notch Chatbot API ready!")

    yield

    # Shutdown
    print("Shutting down Notch Chatbot API...")
    await app.state.sessions.stop_cleanup_task()
    print("✓ Cleanup complete")


# Create FastAPI application
app = FastAPI(
    title="Notch Chatbot API",
    description="Real-time WebSocket API for the Notch AI chatbot",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(APIError, api_error_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

# Include REST routes
app.include_router(router, prefix="/api")

# WebSocket endpoint
app.add_api_websocket_route("/api/ws", websocket_endpoint)


class _BodyOverrideRequest(StarletteRequest):
    """Starlette Request wrapper that returns a pre-set body bytes."""

    def __init__(self, original: Request, body: bytes) -> None:
        super().__init__(original.scope, original.receive)
        self._body = body

    async def body(self) -> bytes:
        return self._body


@app.get("/api/ag-ui/info")
async def ag_ui_info():
    """CopilotKit runtime info endpoint — lists available agents."""
    return JSONResponse(
        {
            "runtimeInfo": {
                "agents": {
                    "default": {
                        "description": "Notch AI assistant for software development agency"
                    }
                }
            }
        }
    )


@app.post("/api/ag-ui")
async def ag_ui_endpoint(request: Request):
    """AG-UI protocol endpoint for CopilotKit integration.

    CopilotKit uses a single-route RPC protocol where every request is a POST
    with a { "method": <name>, "params": {...}, "body": {...} } envelope.

    Supported methods:
      - "info"          → return agent discovery info
      - "agent/connect" → unwrap body and stream agent response via pydantic-ai
    """
    raw = await request.body()
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "method" in data:
            method = data["method"]
            if method == "info":
                # CopilotKit does: const { version, ...runtimeInfo } = response
                # then accesses runtimeInfo.agents — so agents must be at the top level.
                return JSONResponse(
                    {
                        "version": "1.0.0",
                        "agents": {
                            "default": {
                                "description": "Notch AI assistant for software development agency"
                            }
                        },
                    }
                )
            if "body" in data:
                raw = json.dumps(data["body"]).encode()
    except (json.JSONDecodeError, KeyError):
        pass

    return await handle_ag_ui_request(
        agent=request.app.state.agent,
        request=_BodyOverrideRequest(request, raw),
        deps=AgentDeps(kb=request.app.state.kb),
    )
