#!/usr/bin/env python3
"""Test conversation memory."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


import asyncio
import os
from dotenv import load_dotenv
from src.notch_chatbot.agent import create_notch_agent
from src.notch_chatbot.knowledge_base import load_knowledge_base


async def main():
    """Test multi-turn conversation with memory."""
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return

    kb = load_knowledge_base()
    agent = create_notch_agent(kb)

    # Simulate a multi-turn conversation
    conversation = [
        "Do you work with IoT?",
        "Tell me more about that",  # Should reference IoT from previous turn
        "What about AI projects?",
        "Can you give me an example?",  # Should reference AI from previous turn
    ]

    message_history = []

    print("Testing Conversation Memory")
    print("=" * 60)

    for i, user_input in enumerate(conversation, 1):
        print(f"\n[Turn {i}]")
        print(f"You: {user_input}")
        print("Notch: ", end="", flush=True)

        async with agent.run_stream(
            user_input, deps=kb, message_history=message_history
        ) as response:
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)

        print()

        # Update history for next turn
        message_history = response.new_messages()

    print("\n" + "=" * 60)
    print("✓ Memory test complete!")
    print(f"Total messages in history: {len(message_history)}")


if __name__ == "__main__":
    asyncio.run(main())
