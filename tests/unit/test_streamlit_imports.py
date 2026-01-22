#!/usr/bin/env python3
"""Test that Streamlit app imports work correctly."""

print("Testing imports...")

try:
    import streamlit as st  # noqa: F401

    print("✓ streamlit imported")
except ImportError as e:
    print(f"✗ Failed to import streamlit: {e}")
    exit(1)

try:
    from dotenv import load_dotenv  # noqa: F401

    print("✓ dotenv imported")
except ImportError as e:
    print(f"✗ Failed to import dotenv: {e}")
    exit(1)

try:
    from notch_chatbot.agent import create_notch_agent  # noqa: F401

    print("✓ agent module imported")
except ImportError as e:
    print(f"✗ Failed to import agent: {e}")
    exit(1)

try:
    from notch_chatbot.knowledge_base import load_knowledge_base  # noqa: F401

    print("✓ knowledge_base module imported")
except ImportError as e:
    print(f"✗ Failed to import knowledge_base: {e}")
    exit(1)

print("\n✓ All imports successful!")
print("\nYou can now run the Streamlit app with:")
print("  uv run streamlit run streamlit_app.py")
