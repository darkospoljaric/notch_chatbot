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

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
uv sync

# The package will be installed in development mode automatically
```

## Configuration

You'll need an OpenAI API key to run the chatbot:

```bash
export OPENAI_API_KEY=your-api-key-here
```

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
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml.example   # Example secrets file
├── requirements.txt           # Dependencies for Streamlit Cloud
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
- **httpx**: HTTP client for blog fetching
- **uv**: Fast Python package manager

## License

Proprietary - Notch Software Development Agency
