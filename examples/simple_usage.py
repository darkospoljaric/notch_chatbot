#!/usr/bin/env python3
"""
Simple example showing how to use the Notch Chatbot programmatically.

This demonstrates the clean import pattern - no sys.path manipulation needed!
The package is installed via `uv sync`, making imports straightforward.
"""

import asyncio
import os
from dotenv import load_dotenv

# Clean imports from the installed package
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base


async def main():
    """Run a simple chatbot interaction."""
    # Load environment variables
    load_dotenv()

    # Verify API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        print("Create a .env file with: OPENAI_API_KEY=your-key")
        return

    # Load knowledge base and create agent
    print("Loading knowledge base...")
    kb = load_knowledge_base()
    agent = create_notch_agent(kb)
    print(f"✓ Loaded {len(kb.services)} services, {len(kb.case_studies)} case studies\n")

    # Example conversation with memory
    conversation_history = []

    queries = [
        "What do you do?",
        "Do you have IoT experience?",
        "Tell me more about that",  # Tests memory
    ]

    for query in queries:
        print(f"You: {query}")
        print("Notch: ", end="", flush=True)

        # Stream the response
        async with agent.run_stream(
            query, deps=kb, message_history=conversation_history
        ) as response:
            full_response = ""
            async for chunk in response.stream_text(delta=True):
                print(chunk, end="", flush=True)
                full_response += chunk

            # Update conversation history
            conversation_history = response.new_messages()

        print("\n")

    print("✓ Example complete!")


if __name__ == "__main__":
    asyncio.run(main())
