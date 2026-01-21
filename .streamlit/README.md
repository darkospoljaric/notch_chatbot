# Streamlit Configuration

This directory contains configuration files for the Streamlit application.

## Files

### `config.toml`
Main Streamlit configuration including:
- Theme colors and styling
- Server settings
- Port configuration (8501)

### `secrets.toml` (create this for local testing)
Contains sensitive credentials like API keys. This file should **never** be committed to version control.

**To create:**
```bash
cp secrets.toml.example secrets.toml
# Edit secrets.toml and add your actual API key
```

### `secrets.toml.example`
Template showing the required secret format. Safe to commit to git.

## Deployment Notes

For **Streamlit Cloud** deployment:
- Don't create `secrets.toml` in your repository
- Add secrets directly in Streamlit Cloud dashboard:
  1. Go to your app settings
  2. Click "Secrets"
  3. Add your `OPENAI_API_KEY`

For **local development**:
- Create `.streamlit/secrets.toml` with your API key
- Or use `.env` file in project root (also supported)

The `.gitignore` file ensures `secrets.toml` is never committed.
