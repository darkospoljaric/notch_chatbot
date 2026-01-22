#!/usr/bin/env python3
"""Quick test script for the Notch chatbot agent."""

import os

from dotenv import load_dotenv

from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base


def main():
    """Test the agent with a sample query."""
    # Load .env file
    load_dotenv()

    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set")
        return

    print("Loading knowledge base...")
    kb = load_knowledge_base()
    print(
        f"✓ Loaded {len(kb.services)} services, {len(kb.case_studies)} case studies\n"
    )

    print("Creating agent...")
    agent = create_notch_agent(kb)
    print("✓ Agent created\n")

    # Test query
    test_query = "What services do you offer for AI development?"
    print(f"Test Query: {test_query}\n")
    print("Response:")
    print("-" * 60)

    # Run with streaming (synchronous version)
    result = agent.run_sync(test_query, deps=kb)
    # The result is a RunResult object, access the output property
    print(result.output)

    print("\n" + "-" * 60)
    print("\n✓ Test completed successfully!")


if __name__ == "__main__":
    main()
