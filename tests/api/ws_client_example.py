"""Simple WebSocket test client for manual testing.

Usage:
    # Set environment variables
    export API_KEY=test-key-123
    export OPENAI_API_KEY=your-openai-key
    export SENDGRID_API_KEY=your-sendgrid-key

    # Start the server in one terminal
    uv run uvicorn notch_chatbot.api.app:app --reload

    # Run this client in another terminal
    uv run python tests/api/test_ws_client.py
"""

import asyncio
import json
import uuid

import httpx
import websockets


async def test_websocket():
    """Test WebSocket connection and streaming."""
    api_key = "test-key-123"
    base_url = "http://localhost:8000"
    ws_url = "ws://localhost:8000/api/ws"

    print("=" * 60)
    print("Notch Chatbot WebSocket Test Client")
    print("=" * 60)

    # Step 1: Create session
    print("\n1. Creating session...")
    session_id = str(uuid.uuid4())
    print(f"   Session ID: {session_id}")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/api/sessions",
            headers={"X-API-Key": api_key},
            json={"session_id": session_id},
        )
        if response.status_code != 200:
            print(f"   ✗ Failed to create session: {response.text}")
            return
        print(f"   ✓ Session created: {response.json()}")

    # Step 2: Connect WebSocket
    print("\n2. Connecting to WebSocket...")
    headers = {"X-API-Key": api_key, "X-Session-Id": session_id}

    try:
        async with websockets.connect(ws_url, extra_headers=headers) as ws:
            print("   ✓ WebSocket connected")

            # Receive connection ack
            ack = await ws.recv()
            ack_data = json.loads(ack)
            print(f"   ✓ Connection ack: {ack_data}")

            # Step 3: Send first message
            print("\n3. Sending message: 'What services do you offer?'")
            await ws.send(
                json.dumps(
                    {"type": "user_message", "content": "What services do you offer?"}
                )
            )

            # Step 4: Receive streaming response
            print("   Response: ", end="", flush=True)
            full_response = ""
            async for msg_raw in ws:
                msg = json.loads(msg_raw)
                msg_type = msg.get("type")

                if msg_type == "assistant_chunk":
                    chunk = msg.get("content", "")
                    full_response += chunk
                    print(chunk, end="", flush=True)

                elif msg_type == "assistant_complete":
                    print("\n   ✓ Response complete")
                    break

                elif msg_type == "error":
                    print(f"\n   ✗ Error: {msg}")
                    break

            # Step 5: Send follow-up message (test conversation memory)
            print("\n4. Testing conversation memory...")
            print("   Sending: 'Can you tell me more about the first one?'")
            await ws.send(
                json.dumps(
                    {
                        "type": "user_message",
                        "content": "Can you tell me more about the first one?",
                    }
                )
            )

            print("   Response: ", end="", flush=True)
            async for msg_raw in ws:
                msg = json.loads(msg_raw)
                msg_type = msg.get("type")

                if msg_type == "assistant_chunk":
                    chunk = msg.get("content", "")
                    print(chunk, end="", flush=True)

                elif msg_type == "assistant_complete":
                    print("\n   ✓ Response complete")
                    break

                elif msg_type == "error":
                    print(f"\n   ✗ Error: {msg}")
                    break

            print("\n5. Closing connection...")
            await ws.close()
            print("   ✓ Connection closed")

    except Exception as e:
        print(f"\n   ✗ WebSocket error: {e}")
        return

    # Step 6: Check session history
    print("\n6. Checking session history...")
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/api/sessions/{session_id}/history",
            headers={"X-API-Key": api_key},
        )
        if response.status_code == 200:
            history = response.json()
            print(f"   ✓ Messages in history: {history['message_count']}")
        else:
            print(f"   ✗ Failed to get history: {response.text}")

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_websocket())
