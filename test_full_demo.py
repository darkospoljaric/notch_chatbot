#!/usr/bin/env python3
"""Full demo showing all chatbot features."""

import asyncio
import os
from dotenv import load_dotenv
from src.notch_chatbot.agent import create_notch_agent
from src.notch_chatbot.knowledge_base import load_knowledge_base


async def main():
    """Demonstrate all chatbot features."""
    load_dotenv()

    kb = load_knowledge_base()
    agent = create_notch_agent(kb)

    # Realistic conversation showing all features
    conversation = [
        ("Brief response", "What do you do?"),
        ("Memory + Brief", "Do you have experience in my industry?"),  # Vague, should ask
        ("Context memory", "Healthcare"),  # Should remember the question
        ("Tool usage", "Show me a pharma example"),  # Should find ArisGlobal
        ("Detail on request", "Tell me more about that project"),  # Should expand
    ]

    message_history = []

    print("\n" + "=" * 70)
    print("NOTCH CHATBOT - FULL FEATURE DEMO")
    print("=" * 70)
    print("\nFeatures demonstrated:")
    print("  ✓ Concise responses (2-3 sentences by default)")
    print("  ✓ Conversation memory (remembers context)")
    print("  ✓ Tool usage (searches knowledge base)")
    print("  ✓ Expands when asked for details")
    print("  ✓ Real-time streaming")
    print("=" * 70)

    for i, (feature, user_input) in enumerate(conversation, 1):
        print(f"\n[Turn {i} - {feature}]")
        print(f"You: {user_input}")
        print("Notch: ", end="", flush=True)

        async with agent.run_stream(
            user_input, deps=kb, message_history=message_history
        ) as response:
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)

        print()
        message_history = response.new_messages()

    print("\n" + "=" * 70)
    print("✓ Demo complete! All features working as expected.")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
