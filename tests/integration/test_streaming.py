#!/usr/bin/env python3
"""Test streaming functionality."""

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
    """Test streaming with async."""
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return

    print("Loading knowledge base...")
    kb = load_knowledge_base()
    print(f"✓ Loaded {len(kb.services)} services\n")

    print("Creating agent...")
    agent = create_notch_agent(kb)
    print("✓ Agent created\n")

    # Test streaming
    test_query = "Tell me about your experience with IoT solutions and give me a specific example"
    print(f"Query: {test_query}\n")
    print("Streaming response:")
    print("-" * 60)
    print("Notch: ", end="", flush=True)

    async with agent.run_stream(test_query, deps=kb) as response:
        async for chunk in response.stream_text(delta=True):
            print(chunk, end="", flush=True)

    print("\n" + "-" * 60)
    print("\n✓ Streaming test completed!")


if __name__ == "__main__":
    asyncio.run(main())
