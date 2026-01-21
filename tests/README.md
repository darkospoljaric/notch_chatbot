# Test Suite

Comprehensive test suite for the Notch Chatbot.

## Structure

```
tests/
├── unit/              # Unit tests for individual components
├── integration/       # Integration tests for agent behavior
└── demo/             # End-to-end demonstration tests
```

## Test Categories

### Unit Tests (`tests/unit/`)

Test individual components in isolation:

- **verify_kb.py** - Validates knowledge base JSON loading
- **test_streamlit_imports.py** - Checks all imports work correctly

**Run unit tests:**
```bash
uv run python tests/unit/verify_kb.py
uv run python tests/unit/test_streamlit_imports.py
```

### Integration Tests (`tests/integration/`)

Test agent behavior and feature integration:

- **test_agent.py** - Basic agent functionality and responses
- **test_tools.py** - Tool calling and knowledge base search
- **test_concise.py** - Response brevity (2-3 sentences)
- **test_memory.py** - Conversation memory across turns
- **test_streaming.py** - Token streaming functionality

**Run integration tests:**
```bash
uv run python tests/integration/test_agent.py
uv run python tests/integration/test_concise.py
uv run python tests/integration/test_memory.py
# ... etc
```

### Demo Tests (`tests/demo/`)

End-to-end demonstrations showing all features:

- **test_full_demo.py** - Complete feature demonstration
- **test_memory_simple.py** - Simple conversation memory demo
- **test_detailed.py** - Brief vs detailed response examples

**Run demo tests:**
```bash
uv run python tests/demo/test_full_demo.py
uv run python tests/demo/test_memory_simple.py
```

## Running All Tests

### Run entire test suite:
```bash
# Unit tests
for test in tests/unit/*.py; do uv run python "$test"; done

# Integration tests
for test in tests/integration/*.py; do uv run python "$test"; done

# Demo tests
for test in tests/demo/*.py; do uv run python "$test"; done
```

### Using pytest (recommended):
```bash
# Install pytest if not already installed
uv add --dev pytest pytest-asyncio

# Run all tests
uv run pytest tests/

# Run specific category
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/demo/

# Run with verbose output
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src/notch_chatbot
```

## Test Requirements

All tests require:
- OpenAI API key set in `.env` file or environment
- Knowledge base JSON files in `data/` directory
- All dependencies installed (`uv sync`)

**Setup:**
```bash
# Ensure API key is set
echo "OPENAI_API_KEY=your-key" > .env

# Install dependencies
uv sync

# Run tests
uv run pytest tests/
```

## Test Conventions

### File Naming
- All test files start with `test_` prefix
- Descriptive names indicating what is being tested
- Example: `test_memory.py`, `test_agent.py`

### Test Output
- Unit tests: Quick validation, minimal output
- Integration tests: Shows actual agent responses
- Demo tests: Comprehensive output showing all features

### Expected Behavior

**Unit Tests:**
- Should complete in < 5 seconds
- No API calls (mock if needed)
- Test data loading and validation

**Integration Tests:**
- Makes actual API calls
- Takes 10-30 seconds per test
- Tests real agent behavior

**Demo Tests:**
- Comprehensive feature demonstrations
- Takes 30-60 seconds
- Shows complete workflows

## Adding New Tests

### 1. Create Test File

Choose appropriate directory:
- `tests/unit/` - Testing individual functions/components
- `tests/integration/` - Testing agent behavior
- `tests/demo/` - Full feature demonstrations

### 2. Follow Naming Convention

```python
# tests/integration/test_new_feature.py
#!/usr/bin/env python3
"""Test new feature functionality."""

import asyncio
import os
from dotenv import load_dotenv
from src.notch_chatbot.agent import create_notch_agent
from src.notch_chatbot.knowledge_base import load_knowledge_base


async def main():
    """Test new feature."""
    load_dotenv()

    # Your test code here
    pass


if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Make Executable

```bash
chmod +x tests/integration/test_new_feature.py
```

### 4. Document

Add description to this README under appropriate category.

## CI/CD Integration

For automated testing in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    uv sync
    uv run pytest tests/unit/  # Fast unit tests
    # uv run pytest tests/integration/  # Skip in CI (requires API calls)
```

## Troubleshooting

### "API key not found"
```bash
# Check .env file exists and contains key
cat .env | grep OPENAI_API_KEY

# Or export directly
export OPENAI_API_KEY=your-key
```

### "Module not found"
```bash
# Install dependencies
uv sync

# Verify installation
uv run python -c "import src.notch_chatbot"
```

### "Knowledge base error"
```bash
# Verify JSON files are valid
uv run python tests/unit/verify_kb.py
```

### Async runtime errors
```bash
# Ensure using asyncio.run() for async tests
# All integration/demo tests should use async/await
```

## Test Coverage

To generate coverage report:

```bash
# Install coverage tools
uv add --dev pytest-cov

# Run with coverage
uv run pytest tests/ --cov=src/notch_chatbot --cov-report=html

# View report
open htmlcov/index.html
```

## Performance

Expected test execution times:
- **Unit tests**: < 5 seconds total
- **Integration tests**: 2-5 minutes (API calls)
- **Demo tests**: 3-7 minutes (multiple API calls)

For faster development, run unit tests during development and integration tests before commits.
