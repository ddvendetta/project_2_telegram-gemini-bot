# Simple Telegram Bot with Gemini AI

A lightweight Telegram bot powered by Google Gemini API.

## Quick Start (Local Development)

1. **Set environment variables:**
   ```bash
   export TG_BOT_TOKEN="your_telegram_bot_token"
   export GEMINI_API_KEY="your_gemini_api_key"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the bot:**
   ```bash
   python main.py
   ```

## Customization

Edit the `SYSTEM_PROMPT` in `main.py` to customize the bot's behavior:

```python
SYSTEM_PROMPT = """You are a helpful, knowledgeable AI assistant.

Your guidelines:
- Provide clear and accurate information
- Be conversational and professional
- Use examples when helpful
- Format responses for readability
- Acknowledge limitations when needed"""
```

## How It Works

1. User sends a message to the bot on Telegram
2. Bot receives the message and sends it to Gemini API with your custom system prompt
3. Gemini processes and returns a response
4. Bot sends the response back to the user
5. Long messages are automatically split to fit Telegram's 4096 character limit

## Files

- `main.py` - Main bot code (114 lines, simple and clean)
- `requirements.txt` - Python dependencies
- `Procfile` - For Heroku/Railway deployment
- `telegram-bot.service` - For DigitalOcean/Linux systemd
- `DEPLOYMENT_GUIDE.md` - Complete deployment instructions

## Deployment (24/7 Bot)

Choose your preferred platform:

### 🚀 Railway (Recommended - Easiest)
```bash
# 1. Push to GitHub
git push origin main

# 2. Go to Railway.app
# 3. Deploy from GitHub
# 4. Set environment variables
# 5. Done! 24/7 bot running
```

### 🔶 Heroku
```bash
heroku create your-bot-name
heroku config:set TG_BOT_TOKEN="your_token"
heroku config:set GEMINI_API_KEY="your_key"
git push heroku main
```

### 🖥️ DigitalOcean VPS ($4/month)
```bash
# Setup on VPS and use telegram-bot.service file
# Auto-restart on crash, full control
```

**See `DEPLOYMENT_GUIDE.md` for complete deployment instructions with all platforms.**

## How It Works

1. User sends a message to the bot on Telegram
2. Bot receives the message and sends it to Gemini API with your custom system prompt
3. Gemini processes and returns a response
4. Bot sends the response back to the user
5. Long messages are automatically split to fit Telegram's 4096 character limit
