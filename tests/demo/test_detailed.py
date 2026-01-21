#!/usr/bin/env python3
"""Test detailed responses when asked."""


import asyncio
import os
from dotenv import load_dotenv
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base


async def main():
    """Test detailed responses."""
    load_dotenv()

    kb = load_knowledge_base()
    agent = create_notch_agent(kb)

    queries = [
        ("Brief", "What industries do you work with?"),
        ("Detailed", "Tell me more about Spotsie - give me all the details"),
        ("Brief", "Do you do MVPs?"),
        ("Detailed", "Explain your approach to custom software development in detail"),
    ]

    for response_type, query in queries:
        print(f"\n{'='*60}")
        print(f"[{response_type}] Q: {query}")
        print("="*60)
        print("A: ", end="", flush=True)

        async with agent.run_stream(query, deps=kb) as response:
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
