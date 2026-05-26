# Streamlit Cloud Deployment Guide

## Prerequisites
- GitHub repository with your code
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Tavily API key (https://tavily.com)
- Mistral API key (https://console.mistral.ai)

## Deployment Steps

### 1. Push Code to GitHub
```bash
git add -A
git commit -m "prepare for streamlit cloud deployment"
git push
```

### 2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repository
4. Set main file path: `app.py`
5. Click "Advanced settings"
6. Set Python version: `3.11`
7. Click "Deploy"

### 3. Add Secrets

After deployment starts:

1. Click on "Settings" (⚙️) in your app dashboard
2. Go to "Secrets" section
3. Add your API keys in TOML format:

```toml
TAVILY_API_KEY = "your_tavily_api_key_here"
MISTRAL_API_KEY = "your_mistral_api_key_here"
```

4. Click "Save"
5. App will automatically restart with secrets

### 4. Optional: Custom Domain

In app settings, you can configure a custom subdomain like:
`your-app-name.streamlit.app`

## Troubleshooting

### Build Fails
- Check logs in Streamlit Cloud dashboard
- Verify all dependencies in requirements.txt are compatible
- Ensure Python version is 3.11

### API Key Errors
- Verify secrets are added correctly in TOML format
- Check for typos in key names
- Ensure keys are valid and active

### Performance Issues
- Streamlit Cloud free tier has resource limits
- Consider upgrading for production use
- Optimize code to reduce memory usage

## Local Testing Before Deploy

Test with Streamlit secrets locally:

1. Create `.streamlit/secrets.toml` (already in .gitignore)
2. Add your keys:
```toml
TAVILY_API_KEY = "your_key"
MISTRAL_API_KEY = "your_key"
```
3. Run: `streamlit run app.py`

## Notes

- `.env` file is NOT deployed (in .gitignore)
- Secrets are encrypted and secure on Streamlit Cloud
- App auto-updates when you push to GitHub
- Free tier includes: 1GB RAM, shared CPU, community support
