# Usage Examples

This directory contains example scripts showing how to use the Notch Chatbot programmatically.

## Clean Import Pattern

All examples use clean imports from the installed package:

```python
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base
```

**No `sys.path` manipulation needed!** The package is installed in development mode via `uv sync`, making all imports work automatically.

## Running Examples

```bash
# Make sure dependencies are installed
uv sync

# Set your API key
echo "OPENAI_API_KEY=your-key" > .env

# Run an example
uv run python examples/simple_usage.py
```

## Available Examples

### simple_usage.py

Demonstrates basic chatbot usage:
- Loading the knowledge base
- Creating the agent
- Streaming responses
- Maintaining conversation memory

**Output:**
```
Loading knowledge base...
✓ Loaded 11 services, 7 case studies

You: What do you do?
Notch: We specialize in custom software development...

You: Do you have IoT experience?
Notch: Yes, we work with IoT solutions...

You: Tell me more about that
Notch: [References IoT from previous turn with specific examples]
```

## Creating Your Own Scripts

Use this template:

```python
#!/usr/bin/env python3
"""Your script description."""

import asyncio
import os
from dotenv import load_dotenv

# Clean imports - no sys.path needed!
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base


async def main():
    """Your main function."""
    load_dotenv()

    # Load knowledge base
    kb = load_knowledge_base()
    agent = create_notch_agent(kb)

    # Use the agent
    result = agent.run_sync("Your query here", deps=kb)
    print(result.output)


if __name__ == "__main__":
    asyncio.run(main())
```

## Key Points

1. **Package Installation**: Run `uv sync` to install the package in editable mode
2. **Clean Imports**: Import from `notch_chatbot` directly
3. **No Path Hacks**: No `sys.path.insert()` or relative imports needed
4. **API Key**: Set `OPENAI_API_KEY` in `.env` file
5. **Async Support**: Use `asyncio.run()` for async functions

## Testing

All test files in `tests/` directory follow the same clean import pattern:

```bash
# Run tests
./run_tests.sh

# Or individual test
uv run python tests/unit/verify_kb.py
```

See [tests/README.md](../tests/README.md) for more testing information.

## Integration

To integrate the chatbot into your own application:

```python
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base

# Load once at startup
kb = load_knowledge_base()
agent = create_notch_agent(kb)

# Use in your application
def handle_user_query(query: str, history: list):
    result = agent.run_sync(query, deps=kb, message_history=history)
    return result.output
```

Simple, clean, and maintainable!
