#!/usr/bin/env python3
"""Test that agent tools are working correctly."""

import asyncio
import os
from dotenv import load_dotenv
from src.notch_chatbot.agent import create_notch_agent
from src.notch_chatbot.knowledge_base import load_knowledge_base


async def main():
    """Test tool calling."""
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return

    kb = load_knowledge_base()
    agent = create_notch_agent(kb)

    # Test queries that should trigger specific tools
    test_cases = [
        "What services do you offer?",
        "Do you have experience in manufacturing or energy industries?",
        "Tell me about Spotsie",
    ]

    for query in test_cases:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print("="*60)
        print("Response: ", end="", flush=True)

        async with agent.run_stream(query, deps=kb) as response:
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
