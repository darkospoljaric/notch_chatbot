#!/usr/bin/env python3
"""Test that agent gives concise responses."""

import asyncio
import os

from dotenv import load_dotenv

from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base


async def main():
    """Test concise responses."""
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        return

    kb = load_knowledge_base()
    agent = create_notch_agent(kb)

    # Test queries that should get brief responses
    brief_queries = [
        "What do you do?",
        "Do you work with fintech?",
        "Can you help with AI projects?",
        "What's your experience?",
    ]

    # Test query that should get detailed response
    detailed_query = "Tell me more about your AI capabilities and give me examples"

    print("Testing BRIEF responses (should be 2-3 sentences):")
    print("=" * 60)

    for query in brief_queries:
        print(f"\nQ: {query}")
        print("A: ", end="", flush=True)

        async with agent.run_stream(query, deps=kb) as response:
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)
        print("\n")

    print("\n" + "=" * 60)
    print("Testing DETAILED response (should be longer when asked):")
    print("=" * 60)
    print(f"\nQ: {detailed_query}")
    print("A: ", end="", flush=True)

    async with agent.run_stream(detailed_query, deps=kb) as response:
        async for chunk in response.stream_text(delta=True):
            print(chunk, end="", flush=True)
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
