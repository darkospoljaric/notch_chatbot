# FastAPI WebSocket Chat API - Quick Start Guide

## Overview

The Notch Chatbot now has a FastAPI-based API that provides:
- **WebSocket endpoint** at `/api/ws` for real-time streaming chat
- **REST endpoints** for session management
- **API key authentication** for security
- **Coexistence with Streamlit** - both UIs work independently

## Getting Started

### 1. Environment Setup

Ensure `.env` file contains:
```bash
OPENAI_API_KEY=your-openai-key
SENDGRID_API_KEY=your-sendgrid-key
API_KEY=test-key-123  # Set your own secure API key
CORS_ORIGINS=http://localhost:3000,http://localhost:8501
```

### 2. Start the FastAPI Server

```bash
uv run uvicorn notch_chatbot.api.app:app --host 0.0.0.0 --port 8000 --reload
```

Server will start on: http://localhost:8000

### 3. Test the API

#### Health Check (No Auth Required)
```bash
curl http://localhost:8000/api/health
```

#### Create Session
```bash
curl -X POST http://localhost:8000/api/sessions \
  -H "X-API-Key: test-key-123" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "my-unique-session-id"}'
```

Response:
```json
{
  "session_id": "my-unique-session-id",
  "created_at": "2025-02-10T...",
  "expires_in_minutes": 30
}
```

#### Connect WebSocket

Use the provided test client:
```bash
uv run python tests/api/ws_client_example.py
```

Or connect programmatically:
```python
import asyncio
import json
import websockets

async def chat():
    headers = {
        "X-API-Key": "test-key-123",
        "X-Session-Id": "my-unique-session-id"
    }

    async with websockets.connect(
        "ws://localhost:8000/api/ws",
        extra_headers=headers
    ) as ws:
        # Send message
        await ws.send(json.dumps({
            "type": "user_message",
            "content": "What services do you offer?"
        }))

        # Receive streaming response
        async for msg in ws:
            data = json.loads(msg)
            if data["type"] == "assistant_chunk":
                print(data["content"], end="", flush=True)
            elif data["type"] == "assistant_complete":
                break

asyncio.run(chat())
```

## API Endpoints

### REST Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/health` | ❌ No | Server health check |
| POST | `/api/sessions` | ✅ Yes | Create new session |
| GET | `/api/sessions/{id}/history` | ✅ Yes | Get conversation history |
| DELETE | `/api/sessions/{id}` | ✅ Yes | Delete session |

### WebSocket Endpoint

**URL:** `ws://localhost:8000/api/ws`

**Headers Required:**
- `X-API-Key`: Your API key
- `X-Session-Id`: Session ID from POST /api/sessions

**Message Types:**

Client → Server:
```json
{"type": "user_message", "content": "Your question here"}
{"type": "ping"}
```

Server → Client:
```json
{"type": "connection_ack", "session_id": "..."}
{"type": "assistant_chunk", "content": "chunk...", "session_id": "..."}
{"type": "assistant_complete", "content": "full response", "session_id": "..."}
{"type": "error", "error_code": "...", "message": "..."}
{"type": "pong"}
```

## Session Management

### Session Creation Flow

1. **Client generates** a unique session ID (e.g., UUID v4)
2. **Client creates session** via `POST /api/sessions` with session_id in body
3. **Server validates** session_id doesn't already exist
4. **Client connects WebSocket** using the same session_id
5. **Session expires** after 30 minutes of inactivity

### Error Codes

| Error Code | Description |
|------------|-------------|
| `INVALID_API_KEY` | API key is invalid or missing |
| `SESSION_NOT_FOUND` | Session doesn't exist |
| `SESSION_ALREADY_EXISTS` | Session ID is already in use |
| `SESSION_ID_REQUIRED` | Missing session_id in request body |
| `SESSION_EXPIRED` | Session has expired (30 min TTL) |
| `AGENT_ERROR` | AI agent failed to process message |
| `INVALID_MESSAGE` | Malformed request |
| `AGENT_BUSY` | Agent is processing previous message |

## Testing

### Run Unit Tests
```bash
uv run pytest tests/api/test_session_manager.py -v
uv run pytest tests/api/test_auth.py -v
```

### Run Integration Tests
```bash
uv run pytest tests/api/test_rest.py -v
uv run pytest tests/api/test_e2e_simple.py -v
```

### Run All API Tests
```bash
uv run pytest tests/api/ -v
```

### Manual WebSocket Test
```bash
# Start server in one terminal
uv run uvicorn notch_chatbot.api.app:app --reload

# Run test client in another terminal
uv run python tests/api/ws_client_example.py
```

## Architecture

```
src/notch_chatbot/api/
├── __init__.py              # Package exports
├── app.py                   # FastAPI application (lifespan, CORS, routes)
├── websocket.py             # WebSocket endpoint and streaming logic
├── routes.py                # REST endpoints (session CRUD, health)
├── session_manager.py       # In-memory session storage with TTL cleanup
├── models.py               # Pydantic request/response schemas
├── auth.py                  # API key authentication
└── errors.py               # Error codes and exception handlers
```

### Key Features

- **No changes to existing code**: All business logic (agent, tools, services) is reused
- **Streaming responses**: Real-time token streaming via WebSocket
- **Session persistence**: Conversation history maintained per session
- **Concurrent connections**: Multiple WebSocket clients supported
- **Auto-cleanup**: Expired sessions removed every 5 minutes
- **Type-safe**: Pydantic models for all API contracts
- **Testable**: 23 passing tests covering all functionality

## Coexistence with Streamlit

Both interfaces can run simultaneously:

```bash
# Terminal 1: FastAPI server
uv run uvicorn notch_chatbot.api.app:app --port 8000 --reload

# Terminal 2: Streamlit app
uv run streamlit run streamlit_app.py
```

- FastAPI: http://localhost:8000
- Streamlit: http://localhost:8501

Both use the same underlying agent, knowledge base, and business logic.

## Production Deployment

For production, use gunicorn with uvicorn workers:

```bash
gunicorn notch_chatbot.api.app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

**Important Environment Variables:**
- `OPENAI_API_KEY` - Required for AI responses
- `SENDGRID_API_KEY` - Required for proposal emails
- `API_KEY` - Required for authentication
- `CORS_ORIGINS` - Comma-separated allowed origins

## Next Steps

1. **Build a web frontend**: Connect to WebSocket from React/Vue/etc
2. **Mobile app**: Use WebSocket from iOS/Android
3. **API documentation**: Visit http://localhost:8000/docs for auto-generated docs
4. **Rate limiting**: Add rate limiting middleware for production
5. **Database sessions**: Replace in-memory SessionManager with Redis/PostgreSQL

## Troubleshooting

### Server won't start
- Check `.env` file exists and has `OPENAI_API_KEY`
- Ensure port 8000 is not in use: `lsof -i :8000`

### WebSocket connection rejected
- Verify session was created first via REST endpoint
- Check API key matches in both session creation and WebSocket headers
- Ensure session hasn't expired (30 min TTL)

### Agent not responding
- Check `OPENAI_API_KEY` is valid
- Look at server logs for error messages
- Verify knowledge base loaded (check health endpoint)

## Support

For questions or issues:
1. Check the plan.md for detailed implementation notes
2. Review test files for usage examples
3. Run `uv run pytest tests/api/ -v` to verify setup
