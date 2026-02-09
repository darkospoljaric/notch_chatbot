#!/usr/bin/env python3
"""Quick test script for the Notch chatbot agent."""

import os

from dotenv import load_dotenv

from notch_chatbot.adapters.email_adapter import EmailServiceAdapter
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base
from notch_chatbot.services.email_strategy import SendGridEmailService


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

    # Create email adapter (using test API key for integration tests)
    sendgrid_key = os.getenv("SENDGRID_API_KEY", "test_api_key")
    email_service = SendGridEmailService(sendgrid_key)
    email_adapter = EmailServiceAdapter(email_service)

    print("Creating agent...")
    agent = create_notch_agent(email_adapter)
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
