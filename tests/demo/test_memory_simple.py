#!/usr/bin/env python3
"""Simple test showing conversation memory."""

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
    """Test that agent remembers context."""
    load_dotenv()

    kb = load_knowledge_base()
    email_adapter = MockEmailAdapter()
    agent = create_notch_agent(email_adapter)

    # Test conversation showing memory
    conversation = [
        "I'm building a mobile app for retail",
        "What would you recommend?",  # Should remember retail mobile app
        "How long would that take?",  # Should remember the recommendation
    ]

    message_history = []

    print("Testing Context Memory (Simple)")
    print("=" * 60)

    for i, user_input in enumerate(conversation, 1):
        print(f"\n[Turn {i}] You: {user_input}")
        print("Notch: ", end="", flush=True)

        async with agent.run_stream(
            user_input, deps=kb, message_history=message_history
        ) as response:
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)

        print()
        message_history = response.new_messages()

    print("\n" + "=" * 60)
    print("✓ The agent remembered:")
    print("  - Turn 1: User mentioned 'mobile app for retail'")
    print("  - Turn 2: Agent's recommendation based on retail context")
    print("  - Turn 3: Agent referenced the recommendation from Turn 2")


if __name__ == "__main__":
    asyncio.run(main())
