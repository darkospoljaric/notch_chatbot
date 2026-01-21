# Running the Streamlit App

## Quick Start

To run the Notch Chatbot web interface, execute:

```bash
uv run streamlit run streamlit_app.py
```

The app will automatically open in your default browser at `http://localhost:8501`

## What to Expect

When the app starts, you'll see:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

## First Time Setup

1. **Ensure API Key is Set**

   The app needs your OpenAI API key. You have two options:

   **Option A: Using .env file** (Already configured ✓)
   ```bash
   # Your .env file should contain:
   OPENAI_API_KEY=sk-proj-...
   ```

   **Option B: Using Streamlit secrets**
   ```bash
   # Create .streamlit/secrets.toml
   cat > .streamlit/secrets.toml << EOF
   OPENAI_API_KEY = "sk-proj-..."
   EOF
   ```

2. **Open Browser**

   Navigate to `http://localhost:8501` if it doesn't open automatically

3. **Start Chatting**

   Type your message in the input box at the bottom:
   - "What services do you offer?"
   - "Do you have IoT experience?"
   - "Tell me about your AI capabilities"

## Features You'll See

### Chat Interface
- **User messages** appear on the right (gray)
- **Bot responses** appear on the left (white)
- **Streaming** - Watch responses appear letter-by-letter in real-time

### Sidebar (click ≡ to open)
- **About** - Overview of chatbot capabilities
- **Message count** - Track conversation length
- **Clear Chat** button - Start fresh conversation

### Smart Features
- **Context Memory** - Bot remembers previous messages
- **Concise Responses** - Brief by default, detailed when asked
- **Live Examples** - Shows relevant case studies and services

## Stopping the App

Press `Ctrl+C` in the terminal to stop the Streamlit server.

## Troubleshooting

### "API key not found"
- Check your `.env` file exists and contains the correct key
- Verify no extra spaces or quotes around the key value

### Port already in use
If port 8501 is busy, Streamlit will automatically use the next available port (8502, 8503, etc.)

Or specify a different port:
```bash
uv run streamlit run streamlit_app.py --server.port 8502
```

### Module import errors
Run `uv sync` to ensure all dependencies are installed:
```bash
uv sync
```

### Knowledge base not loading
Ensure all JSON files in `data/` directory are valid:
```bash
uv run python verify_kb.py
```

## Production Deployment

For deploying to production (Streamlit Cloud), see:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Complete deployment guide
- [QUICKSTART.md](QUICKSTART.md) - Quick deployment steps

## Need Help?

The app logs appear in your terminal. If you encounter errors:
1. Read the error message in the terminal
2. Check the troubleshooting section above
3. Verify your API key is valid
4. Ensure all dependencies are installed (`uv sync`)
