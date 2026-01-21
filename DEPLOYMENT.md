# Streamlit Deployment Guide

This guide explains how to deploy the Notch Chatbot to Streamlit Cloud.

## 🚀 Quick Deploy

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- OpenAI API key
- SendGrid API key (optional - for automated proposal sending)

### Step 1: Push to GitHub

```bash
# Initialize git repository (if not already done)
git init
git add .
git commit -m "Initial commit"

# Create a new repository on GitHub and push
git remote add origin https://github.com/yourusername/notch-chatbot.git
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository: `yourusername/notch-chatbot`
4. Set main file path: `streamlit_app.py`
5. Click "Advanced settings"
6. Add your secrets:
   ```toml
   # Required
   OPENAI_API_KEY = "your-openai-api-key-here"

   # Optional - for automated PDF proposal generation and email sending
   SENDGRID_API_KEY = "your-sendgrid-api-key-here"
   ```
7. Click "Deploy"

That's it! Your app will be live at `https://yourusername-notch-chatbot.streamlit.app`

## 🧪 Local Testing

To test the Streamlit app locally:

```bash
# Make sure your .env file has OPENAI_API_KEY set
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the Streamlit app
uv run streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔒 Managing Secrets

### For Local Development

Create `.streamlit/secrets.toml`:
```toml
# Required
OPENAI_API_KEY = "your-openai-api-key-here"

# Optional - for automated PDF proposals
SENDGRID_API_KEY = "your-sendgrid-api-key-here"
```

Or use `.env` file (already supported):
```bash
OPENAI_API_KEY=your-openai-api-key-here
SENDGRID_API_KEY=your-sendgrid-api-key-here  # optional
```

### For Streamlit Cloud

1. Go to your app dashboard on Streamlit Cloud
2. Click "Settings" → "Secrets"
3. Add your secrets in TOML format:
   ```toml
   # Required
   OPENAI_API_KEY = "your-openai-api-key-here"

   # Optional - enables automated PDF proposal generation and email sending
   # Get free API key at: https://sendgrid.com (free tier: 100 emails/day)
   # See EMAIL_SETUP.md for detailed setup instructions
   SENDGRID_API_KEY = "your-sendgrid-api-key-here"
   ```
4. Click "Save"

## 📁 Required Files for Deployment

Your repository needs these files:

```
notch-chatbot/
├── streamlit_app.py          # Main Streamlit app (✓ created)
├── requirements.txt           # Dependencies (✓ created)
├── .streamlit/
│   └── config.toml           # Streamlit config (✓ created)
├── src/notch_chatbot/        # Source code (✓ exists)
├── data/                     # Knowledge base JSON files (✓ exists)
└── README.md                 # Documentation (✓ exists)
```

## 🎨 Customization

### Theme Colors

Edit `.streamlit/config.toml` to customize the UI:

```toml
[theme]
primaryColor = "#FF4B4B"        # Primary accent color
backgroundColor = "#FFFFFF"      # Main background
secondaryBackgroundColor = "#F0F2F6"  # Sidebar background
textColor = "#262730"           # Text color
font = "sans serif"             # Font family
```

### App Configuration

Edit `streamlit_app.py` to customize:
- Page title and icon (line 16-18)
- Welcome message (line 106-107)
- Sidebar content (line 169-200)

## 🐛 Troubleshooting

### "API key not found" error
- Check that `OPENAI_API_KEY` is set in Streamlit Cloud secrets
- Verify there are no extra spaces or quotes in the secret value

### "Knowledge base failed to load" error
- Ensure all JSON files in `data/` directory are valid JSON
- Check that the `data/` directory is included in your git repository

### Streaming not working
- Streamlit Cloud supports async streaming out of the box
- If issues persist, check the app logs in Streamlit Cloud dashboard

### Module import errors
- Verify `requirements.txt` includes all necessary dependencies
- Check that the package structure matches what's in the repository

### Email proposals not working
- Ensure `SENDGRID_API_KEY` is set in secrets (optional feature)
- Verify sender email `proposals@wearenotch.com` is verified in SendGrid
- Check app logs for SendGrid API errors
- Without SendGrid configured, bot will work normally but cannot send proposals

## 📧 Email Proposal Feature (Optional)

The chatbot can automatically generate and send professional PDF proposals to prospects:

### Setup Requirements
1. **SendGrid API Key**: Get free account at [sendgrid.com](https://sendgrid.com)
2. **Verify Sender Email**: Must verify `proposals@wearenotch.com` in SendGrid dashboard
3. **Add to Secrets**: Add `SENDGRID_API_KEY` to Streamlit Cloud secrets

### How It Works
- Bot collects prospect name and email during conversation
- Creates professional PDF with project details, pricing, team info
- Automatically sends via email with PDF attachment
- **Auto BCC**: Copies sent to `darko.spoljaric@wearenotch.com` and `sanja.buterin@wearenotch.com`

### Without SendGrid
If not configured, the chatbot:
- Still works fully for conversations
- Cannot send proposals via email
- Will direct prospects to website or contact info

See [EMAIL_SETUP.md](EMAIL_SETUP.md) for detailed setup instructions.

## 📊 Monitoring

Streamlit Cloud provides:
- **Real-time logs**: View in the app dashboard
- **Resource usage**: CPU, memory, and bandwidth metrics
- **Analytics**: Visitor counts and usage patterns

Access these in your app's dashboard on Streamlit Cloud.

## 🔄 Updating Your Deployment

Streamlit Cloud automatically redeploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update chatbot functionality"
git push

# Streamlit Cloud will automatically detect and redeploy
```

## 💰 Cost Considerations

### Streamlit Cloud (Free Tier)
- Hosting: **Free** for public apps
- Limitations: 1GB RAM, shared CPU

### OpenAI API Costs
- GPT-4: ~$0.03 per 1K tokens (input) + $0.06 per 1K tokens (output)
- Average conversation: ~$0.02-0.10 depending on length
- Recommend setting usage limits in OpenAI dashboard

### SendGrid (Free Tier) - Optional
- Email sending: **Free** up to 100 emails/day
- No credit card required for free tier
- Perfect for automated proposal sending
- See [EMAIL_SETUP.md](EMAIL_SETUP.md) for setup instructions

## 🔐 Security Best Practices

1. **Never commit secrets**: Always use Streamlit secrets or environment variables
2. **Use `.gitignore`**: Ensure `.env` and `.streamlit/secrets.toml` are ignored
3. **Rotate API keys**: Regularly rotate your OpenAI API key
4. **Monitor usage**: Set up alerts in OpenAI dashboard for unusual usage
5. **Private repos**: Consider using private GitHub repos for production apps

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Pydantic AI Documentation](https://ai.pydantic.dev)
