# Quick Start Guide

Get the Notch Chatbot running in 3 simple steps.

## 🚀 Local Development

### 1. Install Dependencies

```bash
# Clone the repository
git clone <your-repo-url>
cd notch-chatbot

# Install dependencies using uv
uv sync
```

### 2. Configure API Key

Create a `.env` file:

```bash
echo "OPENAI_API_KEY=your-actual-api-key-here" > .env
```

Or create `.streamlit/secrets.toml`:

```bash
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
OPENAI_API_KEY = "your-actual-api-key-here"
EOF
```

### 3. Run the Chatbot

**Option A: Web UI (Recommended)**

```bash
uv run streamlit run streamlit_app.py
```

Your browser will open to `http://localhost:8501`

**Option B: Terminal CLI**

```bash
uv run notch-chatbot
```

## 🌐 Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- OpenAI API key

### Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/notch-chatbot.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Main file: `streamlit_app.py`
   - Add secret: `OPENAI_API_KEY = "your-key"`
   - Click "Deploy"

3. **Done!**
   Your app will be live at `https://yourusername-notch-chatbot.streamlit.app`

## 🧪 Test the Chatbot

Try these example queries:

1. **General inquiry**: "What services do you offer?"
2. **Industry-specific**: "Do you have experience in healthcare?"
3. **Case study request**: "Show me a fintech example"
4. **Detailed question**: "Tell me more about your AI capabilities"
5. **Follow-up** (tests memory): "Can you give me an example?"

## 📝 Example Conversation

```
You: What do you do?
Notch: We specialize in custom software development, AI systems
(particularly agentic AI), team extension, and enterprise
integrations like Okta and Camunda. Is there a specific type
of project you're interested in?

You: Do you work with healthcare?
Notch: Yes, we have experience in fintech and other regulated
industries including healthcare. Would you like to see a
relevant case study?

You: Yes please
Notch: [Shows ArisGlobal pharma case study with details...]
```

## 🎨 Customization

### Update Knowledge Base

Edit JSON files in `data/` directory:
- `services.json` - Add/edit services
- `case_studies.json` - Add client success stories
- `use_cases.json` - Add use case examples
- `expertise.json` - Update expertise descriptions

Changes take effect on next restart.

### Customize Agent Behavior

Edit `src/notch_chatbot/agent.py`:
- Line 21-98: System prompt and behavior
- Adjust conciseness, tone, or expertise areas

### Customize UI Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
# ... more settings
```

## 🐛 Troubleshooting

**"API key not found"**
- Check `.env` file exists and contains valid key
- For Streamlit Cloud: verify secret is set correctly

**"Module not found"**
- Run `uv sync` to install dependencies
- Ensure you're in the project directory

**Streaming not working**
- Update pydantic-ai: `uv add --upgrade pydantic-ai`
- Check internet connection

**Knowledge base errors**
- Validate JSON files are properly formatted
- Check all required fields are present

## 💡 Tips

- **Cost control**: Set usage limits in OpenAI dashboard
- **Performance**: Knowledge base is cached after first load
- **Memory**: Chat history persists for entire session
- **Mobile**: Streamlit UI is mobile-responsive

## 📚 More Information

- [Full README](README.md) - Complete documentation
- [Deployment Guide](DEPLOYMENT.md) - Detailed deployment instructions
- [Pydantic AI Docs](https://ai.pydantic.dev) - Agent framework documentation
- [Streamlit Docs](https://docs.streamlit.io) - UI framework documentation

## 🆘 Need Help?

1. Check existing issues on GitHub
2. Review the troubleshooting section above
3. Create a new issue with:
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version, etc.)
