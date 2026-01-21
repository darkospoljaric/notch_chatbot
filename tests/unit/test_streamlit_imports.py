#!/usr/bin/env python3
"""Test that Streamlit app imports work correctly."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

print("Testing imports...")

try:
    import streamlit as st
    print("✓ streamlit imported")
except ImportError as e:
    print(f"✗ Failed to import streamlit: {e}")
    exit(1)

try:
    from dotenv import load_dotenv
    print("✓ dotenv imported")
except ImportError as e:
    print(f"✗ Failed to import dotenv: {e}")
    exit(1)

try:
    from src.notch_chatbot.agent import create_notch_agent
    print("✓ agent module imported")
except ImportError as e:
    print(f"✗ Failed to import agent: {e}")
    exit(1)

try:
    from src.notch_chatbot.knowledge_base import load_knowledge_base
    print("✓ knowledge_base module imported")
except ImportError as e:
    print(f"✗ Failed to import knowledge_base: {e}")
    exit(1)

print("\n✓ All imports successful!")
print("\nYou can now run the Streamlit app with:")
print("  uv run streamlit run streamlit_app.py")
