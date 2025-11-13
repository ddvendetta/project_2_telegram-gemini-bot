# Google Cloud Functions Deployment Guide

Deploy your Telegram bot to Google Cloud Functions for free 24/7 hosting!

---

## Prerequisites

- Google Cloud Account (free tier available)
- `gcloud` CLI installed
- Your bot code ready
- Telegram bot token
- Gemini API key

---

## Step 1: Install Google Cloud SDK

### macOS
```bash
brew install --cask google-cloud-sdk
gcloud init
gcloud auth login
```

### Verify Installation
```bash
gcloud --version
gcloud auth list
```

---

## Step 2: Create Google Cloud Project

### Option A: Via Console
1. Go to https://console.cloud.google.com
2. Click project dropdown
3. Click "New Project"
4. Enter project name (e.g., "telegram-bot")
5. Click Create

### Option B: Via CLI
```bash
gcloud projects create telegram-bot --name="Telegram Bot"
gcloud config set project telegram-bot
```

---

## Step 3: Enable Required APIs

```bash
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudscheduler.googleapis.com
```

---

## Step 4: Create Cloud Functions Version of Your Bot

Google Cloud Functions requires a different structure. Create `main_cloud.py`:

```python
import os
import json
import telebot
from google import genai
from google.genai import types
import functions_framework

# Initialize clients
tg_token = os.environ.get("TG_BOT_TOKEN")
gemini_api_key = os.environ.get("GEMINI_API_KEY")

if not tg_token or not gemini_api_key:
    raise ValueError("Missing environment variables")

bot = telebot.TeleBot(tg_token, parse_mode=None)
gemini_client = genai.Client(api_key=gemini_api_key)

# ============================================================================
# CUSTOMIZE YOUR SYSTEM PROMPT HERE
# ============================================================================

SYSTEM_PROMPT = """You are an AI assistant.

Your guidelines:
- Respond in simple terms, short and straight to the point
- No fluff
- Structure long responses into paragraphs of 30 words
- For every response translate into simple iban sarawak language
- For every prompt in other languages, translate it and respond in english"""

# ============================================================================
# End of customization - Don't change below
# ============================================================================


def get_gemini_response(user_message):
    """Send message to Gemini with custom system prompt."""
    try:
        enhanced_prompt = f"""{SYSTEM_PROMPT}

User Question: {user_message}

Please provide a helpful response."""

        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=enhanced_prompt)],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            response_modalities=["TEXT"],
            temperature=0.7,
        )

        response_text = ""
        for chunk in gemini_client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if (chunk.candidates is None or len(chunk.candidates) == 0 or 
                chunk.candidates[0].content is None or 
                chunk.candidates[0].content.parts is None or 
                len(chunk.candidates[0].content.parts) == 0):
                continue
            
            part = chunk.candidates[0].content.parts[0]
            if hasattr(part, 'text') and part.text:
                response_text += part.text
        
        return response_text if response_text else "No response received."
    except Exception as e:
        return f"Error: {str(e)}"


@functions_framework.http
def telegram_webhook(request):
    """HTTP Cloud Function for Telegram webhook."""
    try:
        json_data = request.get_json()
        update = telebot.types.Update.de_json(json_data)
        
        if update.message:
            chat_id = update.message.chat.id
            user_message = update.message.text
            
            # Get response from Gemini
            response = get_gemini_response(user_message)
            
            # Handle long messages
            max_length = 4096
            if len(response) > max_length:
                chunks = [response[i:i+max_length] for i in range(0, len(response), max_length)]
                for chunk in chunks:
                    bot.send_message(chat_id, chunk)
            else:
                bot.send_message(chat_id, response)
        
        return "OK", 200
    except Exception as e:
        print(f"Error: {e}")
        return "Error", 500
```

---

## Step 5: Update requirements.txt

```
pyTelegramBotAPI==4.29.1
google-genai>=0.3.0
functions-framework>=3.0.0
```

---

## Step 6: Deploy Cloud Function

### Set environment variables first:
```bash
export PROJECT_ID="telegram-bot"
export REGION="us-central1"  # Change if needed
export TG_BOT_TOKEN="your_telegram_token"
export GEMINI_API_KEY="your_gemini_api_key"
```

### Deploy the function:
```bash
gcloud functions deploy telegram_webhook \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point telegram_webhook \
  --region $REGION \
  --set-env-vars TG_BOT_TOKEN=$TG_BOT_TOKEN,GEMINI_API_KEY=$GEMINI_API_KEY \
  --source .
```

**Replace:**
- `your_telegram_token` - Your actual Telegram bot token
- `your_gemini_api_key` - Your actual Gemini API key

The deployment takes 2-3 minutes.

---

## Step 7: Get Your Webhook URL

After deployment, get the function URL:

```bash
gcloud functions describe telegram_webhook \
  --region $REGION \
  --format='value(httpsTrigger.url)'
```

This will output something like:
```
https://us-central1-telegram-bot.cloudfunctions.net/telegram_webhook
```

---

## Step 8: Set Telegram Webhook

Set your Telegram bot to use this webhook:

```bash
curl -X POST \
  "https://api.telegram.org/bot$TG_BOT_TOKEN/setWebhook" \
  -d "url=YOUR_FUNCTION_URL"
```

Or use Python:
```python
import requests

url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/setWebhook"
data = {"url": "YOUR_FUNCTION_URL"}
requests.post(url, data=data)
```

---

## Step 9: Test Your Bot

1. Open Telegram
2. Find your bot
3. Send a test message
4. Should get a response immediately

---

## Verify Deployment

### Check function status:
```bash
gcloud functions describe telegram_webhook --region $REGION
```

### View logs:
```bash
gcloud functions logs read telegram_webhook --region $REGION --limit 50
```

### Real-time logs:
```bash
gcloud functions logs read telegram_webhook --region $REGION --follow
```

---

## Update Your Bot

### Method 1: Redeploy with new code
```bash
# Edit main_cloud.py
# Then redeploy:
gcloud functions deploy telegram_webhook \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --source .
```

### Method 2: Change only environment variables
```bash
gcloud functions deploy telegram_webhook \
  --region us-central1 \
  --update-env-vars GEMINI_API_KEY="new_key"
```

---

## Pricing (Google Cloud Functions)

**Free Tier (Always Free):**
- 2 million invocations/month
- 400,000 GB-seconds/month
- 200,000 GB-seconds compute/month

**Perfect for your bot!** Most bots stay well within free tier.

**If you exceed:**
- $0.40 per million invocations
- $0.0000041 per GB-second

---

## Troubleshooting

### Bot not responding

Check logs:
```bash
gcloud functions logs read telegram_webhook --region us-central1 --limit 20
```

### Webhook errors

Verify webhook is set:
```bash
curl https://api.telegram.org/bot$TG_BOT_TOKEN/getWebhookInfo
```

### Environment variables not working

List current env vars:
```bash
gcloud functions describe telegram_webhook --region us-central1
```

### Redeploy from scratch

```bash
# Delete function
gcloud functions delete telegram_webhook --region us-central1

# Redeploy
gcloud functions deploy telegram_webhook \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --set-env-vars TG_BOT_TOKEN=$TG_BOT_TOKEN,GEMINI_API_KEY=$GEMINI_API_KEY \
  --source .
```

---

## Advantages of Google Cloud Functions

✅ **Free tier:** 2M invocations/month (plenty for your bot)
✅ **No server management:** Fully serverless
✅ **Auto-scaling:** Handles traffic spikes
✅ **Easy deployment:** One command
✅ **Integrated logging:** Built-in monitoring
✅ **Reliable:** 99.95% uptime SLA
✅ **Fast:** Responses in milliseconds

---

## Full Setup Script

Create `deploy.sh`:

```bash
#!/bin/bash

set -e

# Configuration
PROJECT_ID="telegram-bot"
REGION="us-central1"
FUNCTION_NAME="telegram_webhook"

# Get credentials
TG_BOT_TOKEN=$1
GEMINI_API_KEY=$2

if [ -z "$TG_BOT_TOKEN" ] || [ -z "$GEMINI_API_KEY" ]; then
    echo "Usage: ./deploy.sh <TELEGRAM_TOKEN> <GEMINI_API_KEY>"
    exit 1
fi

echo "Setting up Google Cloud Functions..."
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo ""

# Set project
gcloud config set project $PROJECT_ID

# Enable APIs
echo "Enabling APIs..."
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Deploy function
echo "Deploying function..."
gcloud functions deploy $FUNCTION_NAME \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region $REGION \
  --set-env-vars TG_BOT_TOKEN=$TG_BOT_TOKEN,GEMINI_API_KEY=$GEMINI_API_KEY \
  --source .

# Get URL
echo ""
echo "✅ Deployment complete!"
echo ""
echo "Getting webhook URL..."
URL=$(gcloud functions describe $FUNCTION_NAME \
  --region $REGION \
  --format='value(httpsTrigger.url)')

echo "Webhook URL: $URL"
echo ""
echo "Setting Telegram webhook..."
curl -X POST \
  "https://api.telegram.org/bot$TG_BOT_TOKEN/setWebhook" \
  -d "url=$URL"

echo ""
echo "✅ All done! Your bot is now live!"
echo "Test it by sending a message to your Telegram bot."
```

Make it executable:
```bash
chmod +x deploy.sh
```

Run it:
```bash
./deploy.sh "YOUR_TELEGRAM_TOKEN" "YOUR_GEMINI_API_KEY"
```

---

## Monitoring Your Bot

### View all functions:
```bash
gcloud functions list --region us-central1
```

### Check execution logs:
```bash
gcloud functions logs read telegram_webhook --region us-central1 --follow
```

### Check errors:
```bash
gcloud functions logs read telegram_webhook --region us-central1 --min-log-level ERROR
```

### Check invocations:
Visit Cloud Console → Cloud Functions → Select function → Logs tab

---

## Updating Your Bot

### Step 1: Edit main_cloud.py (e.g., change SYSTEM_PROMPT)

### Step 2: Redeploy
```bash
gcloud functions deploy telegram_webhook \
  --runtime python312 \
  --trigger-http \
  --region us-central1 \
  --source .
```

Done! Changes take effect immediately.

---

## Delete Your Bot (If Needed)

```bash
gcloud functions delete telegram_webhook --region us-central1

# Also remove webhook from Telegram
curl -X POST \
  "https://api.telegram.org/bot$TG_BOT_TOKEN/deleteWebhook"
```

---

## Cost Breakdown

| Usage | Monthly Cost |
|-------|---|
| 1,000 messages/day | **Free** |
| 10,000 messages/day | **Free** |
| 100,000 messages/day | **Free** |
| 2,000,000 messages/month (limit) | **Free** |
| 10,000,000 messages/month | ~$3 |

Most bots stay in the **free tier forever**.

---

## Key Differences: Cloud Functions vs VPS

| Feature | Cloud Functions | VPS (DigitalOcean) |
|---------|---|---|
| Cost | Free (2M/month) | $4/month |
| Setup | 1 command | 10 minutes |
| Management | None | Need to manage |
| Scaling | Automatic | Manual |
| Cold start | ~1 second | Instant |
| Uptime | 99.95% | 99.9% |

**Best for:** Most users, webhook-based architecture
**Recommended:** Google Cloud Functions (simplest)

---

## Summary

Your bot on Google Cloud Functions:

1. ✅ Runs 24/7
2. ✅ Completely free (under 2M invocations/month)
3. ✅ Automatic scaling
4. ✅ No server management
5. ✅ Easy to update
6. ✅ Built-in monitoring

**Next Step:** Follow the deployment steps above!

---

## Quick Checklist

Before deploying:
- [ ] Google Cloud account created
- [ ] Project created
- [ ] `gcloud` CLI installed and authenticated
- [ ] `main_cloud.py` created and tested locally
- [ ] `requirements.txt` updated with `functions-framework`
- [ ] Telegram bot token ready
- [ ] Gemini API key ready

Deployment steps:
- [ ] Enable APIs
- [ ] Deploy function (one command)
- [ ] Get webhook URL
- [ ] Set webhook in Telegram
- [ ] Test with a message

Done! Your bot runs 24/7 for free! 🎉

---

## Help & Resources

- [Google Cloud Functions Docs](https://cloud.google.com/functions/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Cloud Console](https://console.cloud.google.com)

Questions? Check the troubleshooting section above!
