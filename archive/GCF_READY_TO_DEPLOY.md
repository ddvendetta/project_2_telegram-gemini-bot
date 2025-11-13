# 🚀 Google Cloud Functions Deployment - Complete Setup

Your Telegram bot is ready to deploy to Google Cloud Functions for **24/7 production hosting**.

## What's New

Three files have been created for easy Google Cloud Functions deployment:

### 1. **deploy_cloud.sh** - Automated Deployment Script
An executable bash script that automates the entire deployment process.

**What it does:**
- Validates gcloud installation
- Sets up your GCP project
- Enables required APIs
- Deploys the Cloud Function
- Sets up Telegram webhook automatically
- Provides webhook URL and status

**How to use:**
```bash
./deploy_cloud.sh PROJECT_ID REGION BOT_TOKEN API_KEY
```

**Example:**
```bash
./deploy_cloud.sh my-telegram-bot us-central1 "123456:ABCDEFghijklmnop" "AIzaSyD..."
```

### 2. **main_cloud.py** - Webhook-Based Bot Code
The bot code configured for Google Cloud Functions (webhook architecture).

**Differences from main.py:**
- Uses `@functions_framework.http` decorator
- Receives HTTP requests (webhooks) instead of polling
- More efficient and cost-effective
- Identical bot logic to main.py
- Auto-scales with Google Cloud infrastructure

**Key features:**
- Same SYSTEM_PROMPT (customizable at line 28-37)
- Same Gemini AI integration
- Automatic message splitting (handles Telegram's 4096 char limit)
- Error handling and logging
- Environment variable support

### 3. **requirements_cloud.txt** - GCF Dependencies
Python packages needed for Cloud Functions deployment.

**Packages:**
- `pyTelegramBotAPI==4.29.1` - Telegram integration
- `google-genai>=0.3.0` - Gemini API
- `functions-framework>=3.0.0` - Google Cloud Functions runtime

### 4. **QUICK_GCF_DEPLOY.md** - 5-Minute Guide
Fast deployment guide without all the details.

---

## Deployment Steps

### Step 1: Prepare Your Machine
```bash
# Install Google Cloud SDK (if needed)
brew install google-cloud-sdk

# Authenticate
gcloud init
gcloud auth login
```

### Step 2: Get Your Credentials
- **Telegram Bot Token**: Message @BotFather on Telegram
- **Gemini API Key**: Get from [ai.google.dev](https://ai.google.dev)
- **GCP Project ID**: Any unique name (e.g., `my-telegram-bot`)

### Step 3: Deploy (One Command!)
```bash
./deploy_cloud.sh YOUR_PROJECT_ID us-central1 YOUR_BOT_TOKEN YOUR_API_KEY
```

The script will:
1. Create/set up your GCP project
2. Enable required APIs
3. Deploy the Cloud Function (~2-3 minutes)
4. Configure Telegram webhook
5. Show you the live URL

### Step 4: Test
- Open Telegram
- Send a message to your bot
- Should get a response in seconds

---

## File Structure

```
Your Project:
├── main.py                          ✅ Local/VPS version (polling)
├── main_cloud.py                    ✅ NEW: Cloud Functions version (webhook)
├── requirements.txt                 ✅ Standard dependencies
├── requirements_cloud.txt           ✅ NEW: Cloud Functions dependencies
├── deploy_cloud.sh                  ✅ NEW: Automated deployment script
├── QUICK_GCF_DEPLOY.md              ✅ NEW: Quick 5-minute guide
├── GCF_DEPLOYMENT_GUIDE.md          📖 Detailed deployment guide
├── DEPLOYMENT_GUIDE.md              📖 Other platforms (Heroku, Railway, etc.)
├── QUICK_DEPLOY.md                  📖 Quick start for all platforms
├── Procfile                         ✅ For Heroku/Railway
└── telegram-bot.service             ✅ For Linux VPS
```

---

## Pricing (Google Cloud Functions)

**Free tier (always free):**
- 2 million invocations per month
- 400,000 GB-seconds per month
- Great for bots!

**Example costs:**
| Usage | Monthly Cost |
|-------|-------------|
| 100 messages/day | FREE ✅ |
| 1,000 messages/day | FREE ✅ |
| 10,000 messages/day | ~$0.40 |
| 100,000 messages/day | ~$4 |

**You only pay if you exceed free tier limits!**

---

## Key Advantages of Google Cloud Functions

✅ **No servers to manage** - Google handles scaling  
✅ **Always on** - 24/7 availability with 99.95% uptime SLA  
✅ **Auto-scaling** - Handles traffic spikes automatically  
✅ **Cheap** - Free tier is very generous  
✅ **Simple** - One command deployment with automated webhook setup  
✅ **Monitoring** - Built-in logs and metrics  
✅ **Secure** - Google Cloud security infrastructure  

---

## Customization

### Change the Bot Response

Edit `main_cloud.py` at **line 28-37** (SYSTEM_PROMPT):

```python
SYSTEM_PROMPT = """You are a helpful assistant...
... your custom system prompt here ...
"""
```

Then redeploy:
```bash
./deploy_cloud.sh my-telegram-bot us-central1 "BOT_TOKEN" "API_KEY"
```

### Change the Bot Name

Edit the webhook function name in `main_cloud.py` line 83:
```python
@functions_framework.http
def telegram_webhook(request):
```

Then update the deploy script:
```bash
gcloud functions deploy your_new_name \
  --runtime python312 \
  --trigger-http \
  --region us-central1 \
  ...
```

---

## Troubleshooting

### "gcloud: command not found"
Install Google Cloud SDK: `brew install google-cloud-sdk`

### "Project not found"
Make sure your project ID matches and you've run `gcloud init`

### "Webhook URL is not responding"
- Wait 2-3 minutes for deployment to complete
- Check logs: `gcloud functions logs read telegram_webhook --region us-central1`

### "Bot not responding in Telegram"
- Verify webhook was set: Check deployment script output for "ok":true
- Check logs for errors: `gcloud functions logs read telegram_webhook --region us-central1 --limit 50`
- Verify credentials (tokens) are correct

### Update Bot Code
Edit `main_cloud.py`, then:
```bash
./deploy_cloud.sh my-telegram-bot us-central1 "BOT_TOKEN" "API_KEY"
```

### View Live Logs
```bash
gcloud functions logs read telegram_webhook --region us-central1 --follow
```

---

## Alternative Deployment Options

Not sure about Google Cloud Functions? See other options:

- **Railway** - Quick, easy, generous free tier
- **Heroku** - Classic, now paid starting at $7/month
- **DigitalOcean** - Cheap VPS at $4/month
- **PythonAnywhere** - Python-specific hosting
- **Replit** - Browser-based, very simple

See **DEPLOYMENT_GUIDE.md** for all options.

---

## Next Steps

### Immediate:
1. Have your bot token and API key ready
2. Run the deployment script
3. Test your bot

### After Deployment:
1. Monitor logs regularly
2. Update bot code as needed
3. Scale up if needed (GCF handles auto-scaling)

### If Something Changes:
1. Update credentials: Use deploy script with new values
2. Update code: Edit main_cloud.py, redeploy
3. Switch platforms: See DEPLOYMENT_GUIDE.md

---

## Summary

You now have everything needed for **production-grade, 24/7 bot hosting** on Google Cloud Functions:

✅ **Automated deployment** - `deploy_cloud.sh`  
✅ **Production code** - `main_cloud.py`  
✅ **Fast guide** - `QUICK_GCF_DEPLOY.md`  
✅ **Detailed docs** - `GCF_DEPLOYMENT_GUIDE.md`  
✅ **Free tier** - 2M invocations/month  
✅ **Monitoring** - Integrated logging and metrics  

**Ready to deploy? Run:**
```bash
./deploy_cloud.sh my-telegram-bot us-central1 "YOUR_BOT_TOKEN" "YOUR_API_KEY"
```

---

**Questions? Check GCF_DEPLOYMENT_GUIDE.md for detailed troubleshooting.**

**Happy deploying! 🚀**
