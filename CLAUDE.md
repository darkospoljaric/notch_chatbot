# Claude AI Assistant Guidelines for Notch Chatbot

This document provides specific instructions and context for Claude (AI assistants) working on the Notch Chatbot project.

## Project Overview

This is an AI-powered chatbot for Notch Software Development Agency. The chatbot helps potential clients understand Notch's capabilities, explore case studies, and guides conversations toward appointments or proposals.

**Key Technologies:**
- Python 3.13+
- Pydantic AI (agent framework)
- OpenAI GPT-4o
- Streamlit (web UI)
- uv (package manager)

## Critical Conversation Guardrails

The chatbot has **strict scope restrictions** defined in `src/notch_chatbot/agent.py`:

### What the Bot MUST Discuss
- Notch's services and capabilities
- Notch's case studies and projects
- How Notch can help prospective clients
- Scheduling calls and sending proposals
- Technologies/approaches in the context of Notch's offerings

### What the Bot MUST NOT Discuss
- Other companies or competitors
- General technology advice unrelated to Notch
- Personal topics, current events, politics
- Any subject matter outside Notch's business

**When modifying the agent, these guardrails MUST be maintained.**

## Key Behavioral Requirements

### 1. Brevity Rule (CRITICAL)
The chatbot MUST default to **2-3 sentences maximum** for every response throughout the entire conversation. It only expands when users explicitly ask with phrases like:
- "Tell me more"
- "Explain in detail"
- "Give me details"
- "Can you elaborate"

This rule applies to ALL responses, not just initial ones.

### 2. Conversation Convergence
The chatbot should guide conversations toward concrete actions:
1. **Schedule a call** (primary goal for qualified prospects)
2. **Send proposal via email** (secondary goal)
3. **Provide contact info** (fallback)

After 3-5 engaged exchanges, the bot should proactively suggest next steps.

### 3. Automated Offer Creation
The bot uses `create_and_send_offer` tool to generate and email PDF proposals automatically when:
- User provides name and email
- Project needs are understood
- User shows interest in next steps

## Development Guidelines

### Environment Setup

```bash
# Install dependencies
uv sync

# Set required API key
export OPENAI_API_KEY=your-key-here

# Optional: Email functionality
export SENDGRID_API_KEY=your-mailersend-key-here
```

### Running the Application

```bash
# Web UI (recommended)
uv run streamlit run streamlit_app.py

# CLI
uv run notch-chatbot
```

### Testing

```bash
# Run all tests
./run_tests.sh

# Run specific test categories
./run_tests.sh unit
./run_tests.sh integration
./run_tests.sh demo

# Email integration test (requires SENDGRID_API_KEY)
pytest tests/integration/test_email_send.py --run-email -v
```

### Linting and Formatting

```bash
# Check linting
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

## Code Modification Guidelines

### When Modifying the Agent (`src/notch_chatbot/agent.py`)

1. **NEVER remove or weaken conversation guardrails**
2. **NEVER change the brevity rule** (2-3 sentences default)
3. **NEVER remove the action convergence logic** (guiding to calls/proposals)
4. Test changes thoroughly with integration tests
5. Ensure the system prompt remains clear and enforceable

### When Modifying Knowledge Base (`data/*.json`)

The knowledge base consists of:
- `services.json` - Service offerings
- `case_studies.json` - Customer success stories
- `use_cases.json` - Specific use case examples
- `expertise.json` - Technical expertise domains

**Structure requirements:**
- Maintain existing JSON schema
- All IDs must be unique and kebab-case
- URLs must be valid and point to wearenotch.com
- Run `uv run python tests/unit/verify_kb.py` after changes

### When Adding New Tools (`src/notch_chatbot/tools.py`)

1. Use Pydantic models for type safety
2. Return structured data, not formatted strings
3. Document tool purpose clearly in docstrings
4. Register new tools in `create_notch_agent()` function
5. Add corresponding unit tests in `tests/unit/`
6. Add integration tests in `tests/integration/test_tools.py`

### When Modifying the Streamlit UI (`streamlit_app.py`)

1. Maintain real-time streaming functionality
2. Keep conversation memory intact
3. Test mobile responsiveness
4. Ensure session state management works correctly
5. Test with `tests/unit/test_streamlit_imports.py`

## Common Tasks

### Adding a New Service

1. Edit `data/services.json`
2. Follow existing schema structure
3. Verify with: `uv run python tests/unit/verify_kb.py`
4. Test agent can find it: `uv run python tests/integration/test_tools.py`

### Adding a Case Study

1. Edit `data/case_studies.json`
2. Include industry, service mapping, and outcomes
3. Verify JSON is valid
4. Test retrieval through agent tools

### Updating System Prompt

1. Edit `SYSTEM_PROMPT` in `src/notch_chatbot/agent.py`
2. **CRITICAL:** Maintain all guardrails and behavioral rules
3. Test with: `uv run python tests/integration/test_agent.py`
4. Test brevity with: `uv run python tests/integration/test_concise.py`
5. Test memory with: `uv run python tests/integration/test_memory.py`

### Debugging Agent Behavior

1. Check system prompt in `agent.py` first
2. Use demo tests to see full conversation flow:
   ```bash
   uv run python tests/demo/test_full_demo.py
   ```
3. Test specific tools:
   ```bash
   uv run python tests/integration/test_tools.py -v
   ```
4. Enable verbose logging in integration tests

## Project Structure

```
notch_chatbot/
├── src/notch_chatbot/
│   ├── agent.py           # Main agent with SYSTEM_PROMPT (CRITICAL)
│   ├── tools.py           # Agent tools for KB search
│   ├── models.py          # Pydantic data models
│   ├── knowledge_base.py  # KB loader
│   └── cli.py             # CLI interface
├── data/                  # Knowledge base JSON files
├── tests/
│   ├── unit/             # Fast tests, no API calls
│   ├── integration/      # Agent behavior tests
│   └── demo/             # End-to-end demos
├── streamlit_app.py      # Web UI (main entry point)
└── examples/             # Usage examples
```

## Important Files to Understand

1. **`src/notch_chatbot/agent.py`** - Contains SYSTEM_PROMPT with all behavioral rules
2. **`src/notch_chatbot/tools.py`** - All agent tools for searching knowledge base
3. **`data/services.json`** - Service offerings that bot can reference
4. **`data/case_studies.json`** - Case studies for social proof
5. **`streamlit_app.py`** - Web UI with streaming and memory

## Testing Strategy

- **Unit tests**: Fast, no API calls, test individual components
- **Integration tests**: Test agent behavior with real LLM calls (requires OPENAI_API_KEY)
- **Demo tests**: Full conversation flows for manual verification

Always run tests before committing changes:
```bash
./run_tests.sh
```

## Deployment

The application is designed for Streamlit Cloud deployment. See `DEPLOYMENT.md` for detailed instructions.

**Required secrets in Streamlit Cloud:**
- `OPENAI_API_KEY` (required)
- `SENDGRID_API_KEY` (optional, for email proposals)

## Security Considerations

1. **Never commit API keys** - Use `.env` or Streamlit secrets
2. **Validate all user inputs** in tools
3. **Maintain conversation scope restrictions** to prevent misuse
4. **Test email functionality** carefully to avoid spam issues
5. **Review knowledge base** for sensitive information before deployment

## When in Doubt

1. Read the system prompt in `agent.py` - it's the source of truth
2. Run the demo tests to see expected behavior
3. Check existing test cases for patterns
4. Maintain the three core principles:
   - **Strict scope** (only Notch topics)
   - **Brief responses** (2-3 sentences default)
   - **Action convergence** (guide to calls/proposals)

## Contact

For questions about this project, refer to:
- `README.md` - General project documentation
- `PROJECT_SUMMARY.md` - Detailed project summary
- `NEXT_STEPS.md` - Planned improvements
- `tests/README.md` - Testing documentation

---

**Remember:** The chatbot's personality and guardrails are NOT negotiable. They are core to the product's value proposition and must be preserved in all modifications.
