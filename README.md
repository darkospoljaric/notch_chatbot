# Notch Chatbot

AI-powered chatbot assistant for Notch software development agency. This chatbot helps potential clients understand Notch's capabilities, explore relevant case studies, and get information about services.

## Features

- 🤖 Conversational AI assistant powered by GPT-4
- 📚 Knowledge base with services, case studies, and use cases
- 🔍 Intelligent matching of client needs to relevant examples
- 💬 Consultative approach (helpful, not pushy)
- ⚡ Token streaming for real-time responses
- 🧠 Conversation memory - maintains context across the entire chat session
- 💡 Concise by default - expands only when asked for details
- 📧 **Automated Proposals** - Creates and emails professional PDF proposals with pricing
- 🎯 **Lead Conversion** - Guides conversations toward appointments and proposals

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# The package will be installed in development mode automatically
```

## Configuration

### Required: OpenAI API Key

You'll need an OpenAI API key to run the chatbot:

```bash
export OPENAI_API_KEY=your-api-key-here
```

Or create a `.env` file in the project root:

```
OPENAI_API_KEY=your-api-key-here
```

### Optional: Email Proposals (SendGrid)

To enable automated PDF proposal generation and sending, set up SendGrid (free tier available):

```
SENDGRID_API_KEY=your-sendgrid-api-key
```

Proposals are automatically sent from `proposals@wearenotch.com` (hardcoded).

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed setup instructions.

**Without SendGrid configured**: The chatbot will work normally but cannot send proposals. It will inform prospects to visit the website or contact directly.

## Usage

### Option 1: Streamlit Web UI (Recommended)

Run the interactive web interface:

```bash
uv run streamlit run streamlit_app.py
```

This will open a web browser with a beautiful chat interface featuring:
- 💬 Real-time streaming responses
- 🧠 Full conversation memory
- 📱 Mobile-friendly design
- 🎨 Clean, modern UI

**Deploy to Streamlit Cloud**: See [DEPLOYMENT.md](DEPLOYMENT.md) for instructions on deploying to Streamlit's free hosting.

### Option 2: Command Line Interface

Run the chatbot in your terminal:

```bash
uv run notch-chatbot
```

Or if you've activated the virtual environment:

```bash
notch-chatbot
```

The chatbot will start and you can begin conversing. Example interactions:

- "What services do you offer?"
- "Do you have experience in fintech?"
- "Tell me about your AI capabilities"
- "I need a mobile app for my retail business"
- "What's your experience with legacy system modernization?"

Type `exit`, `quit`, or press `Ctrl+C` to end the session.

## Project Structure

```
notch-chatbot/
├── streamlit_app.py           # Streamlit web UI (main entry point)
├── src/
│   └── notch_chatbot/
│       ├── __init__.py
│       ├── models.py          # Pydantic data models
│       ├── knowledge_base.py  # KB loader from JSON
│       ├── tools.py           # Agent tools for searching KB
│       ├── agent.py           # Main Pydantic AI agent
│       └── cli.py             # CLI interface
├── data/
│   ├── services.json          # Service offerings
│   ├── case_studies.json      # Customer success stories
│   ├── use_cases.json         # Use case examples
│   └── expertise.json         # Expertise domain descriptions
├── tests/                     # Test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   ├── demo/                  # Demo tests
│   └── README.md              # Test documentation
├── examples/                  # Usage examples
│   ├── simple_usage.py        # Basic usage example
│   └── README.md              # Examples documentation
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml.example   # Example secrets file
├── requirements.txt           # Dependencies for Streamlit Cloud
├── pytest.ini                 # Pytest configuration
├── run_tests.sh              # Test runner script
├── pyproject.toml            # Project configuration
├── DEPLOYMENT.md             # Deployment guide
└── README.md
```

## Knowledge Base

The chatbot's knowledge is stored in JSON files in the `data/` directory:

- **services.json**: All service offerings (custom dev, AI, MVP, etc.)
- **case_studies.json**: Customer success stories with industries and outcomes
- **use_cases.json**: Specific use cases demonstrating capabilities
- **expertise.json**: Descriptions of technical expertise domains

To update the knowledge base, edit the JSON files. Changes take effect on next startup.

## Programmatic Usage

For using the chatbot in your own code, see the `examples/` directory:

```python
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base

# Load knowledge base and create agent
kb = load_knowledge_base()
agent = create_notch_agent(kb)

# Use the agent
result = agent.run_sync("What services do you offer?", deps=kb)
print(result.output)
```

See [examples/README.md](examples/README.md) for more examples and patterns.

## Development

### Adding New Services

Edit `data/services.json` following the existing structure:

```json
{
  "id": "unique-service-id",
  "name": "Service Name",
  "category": "build",
  "description": "Detailed description...",
  "short_description": "Brief 1-2 sentence summary",
  "key_features": ["Feature 1", "Feature 2"],
  "related_expertise": ["software_engineering", "ai_engineering"],
  "ideal_for": ["Scenario 1", "Scenario 2"],
  "url": "https://www.wearenotch.com/services/..."
}
```

### Adding Case Studies

Edit `data/case_studies.json` with relevant customer stories.

### Customizing Agent Behavior

The system prompt and agent configuration are in `src/notch_chatbot/agent.py`.

## Technologies

- **Python 3.13+**
- **Pydantic AI**: Agent framework with tool calling
- **OpenAI GPT-4**: Language model
- **Streamlit**: Web UI framework
- **httpx**: HTTP client for blog fetching
- **uv**: Fast Python package manager
- **pytest**: Testing framework (dev)

## Testing

The project includes a comprehensive test suite organized by category:

```
tests/
├── unit/              # Unit tests (fast, no API calls)
├── integration/       # Integration tests (agent behavior)
└── demo/             # End-to-end demonstrations
```

### Run All Tests

```bash
# Using the test runner script
./run_tests.sh

# Or run specific categories
./run_tests.sh unit
./run_tests.sh integration
./run_tests.sh demo

# Using pytest
uv run pytest tests/
uv run pytest tests/unit/
uv run pytest tests/integration/
```

### Quick Validation

```bash
# Verify knowledge base
uv run python tests/unit/verify_kb.py

# Test agent responses
uv run python tests/integration/test_agent.py

# See full demo
uv run python tests/demo/test_full_demo.py
```

**Import Pattern**: Tests use clean imports from the installed package:
```python
from notch_chatbot.agent import create_notch_agent
from notch_chatbot.knowledge_base import load_knowledge_base
```

No `sys.path` manipulation needed - the package is installed via `uv sync`!

See [tests/README.md](tests/README.md) for detailed testing documentation.

## License

Proprietary - Notch Software Development Agency
