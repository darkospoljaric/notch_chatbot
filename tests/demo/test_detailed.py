#!/usr/bin/env python3
"""Test detailed responses when asked."""

import asyncio

from dotenv import load_dotenv

from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base


class MockEmailAdapter:
    """Mock email adapter for demo tests."""

    async def send_proposal(
        self, client_name: str, client_email: str, pdf_content: bytes, project_summary: str
    ) -> tuple[bool, str]:
        """Mock send - just returns success without sending."""
        return True, f"[DEMO MODE] Would send proposal to {client_email}"


async def main():
    """Test detailed responses."""
    load_dotenv()

    kb = load_knowledge_base()
    email_adapter = MockEmailAdapter()
    agent = create_notch_agent(email_adapter)

    queries = [
        ("Brief", "What industries do you work with?"),
        ("Detailed", "Tell me more about Spotsie - give me all the details"),
        ("Brief", "Do you do MVPs?"),
        ("Detailed", "Explain your approach to custom software development in detail"),
    ]

    for response_type, query in queries:
        print(f"\n{'=' * 60}")
        print(f"[{response_type}] Q: {query}")
        print("=" * 60)
        print("A: ", end="", flush=True)

        async with agent.run_stream(query, deps=kb) as response:
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
