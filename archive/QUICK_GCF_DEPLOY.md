# ⚡ Quick Google Cloud Functions Deployment (5 Minutes)

Deploy your Telegram bot to Google Cloud Functions in **5 minutes** using the automated script.

## Prerequisites
- ✅ Telegram bot token from @BotFather
- ✅ Gemini API key from [ai.google.dev](https://ai.google.dev)
- ✅ Google Cloud account (free tier available)
- ✅ Google Cloud SDK installed (`gcloud` command)

### Install Google Cloud SDK (if needed)
```bash
# macOS
brew install google-cloud-sdk

# Or download from:
# https://cloud.google.com/sdk/docs/install
```

## One-Step Deployment

```bash
# Make script executable
chmod +x deploy_cloud.sh

# Run deployment script
./deploy_cloud.sh YOUR_PROJECT_ID REGION YOUR_BOT_TOKEN YOUR_API_KEY
```

### Example:
```bash
./deploy_cloud.sh my-telegram-bot us-central1 "123456:ABCDEFghijklmnop" "AIzaSyD..."
```

### Parameters:
- **PROJECT_ID**: Unique name for your GCP project (e.g., `my-telegram-bot`)
- **REGION**: GCP region (use `us-central1` if unsure)
- **BOT_TOKEN**: From @BotFather on Telegram
- **API_KEY**: From Google AI Studio

## What Happens Automatically

The script will:
1. ✅ Validate gcloud installation
2. ✅ Set your Google Cloud project
3. ✅ Enable required APIs
4. ✅ Deploy Cloud Function (takes ~2-3 minutes)
5. ✅ Configure Telegram webhook automatically
6. ✅ Display webhook URL
7. ✅ Test webhook setup

## Test Your Bot

**In Telegram:**
1. Open your bot chat
2. Send any message
3. Should get a response in seconds

**View logs:**
```bash
gcloud functions logs read telegram_webhook --region us-central1 --follow
```

## Pricing

**Free tier includes:**
- 2,000,000 invocations/month (free forever)
- 400,000 GB-seconds/month
- 24 GB/month outbound network

**Cost for typical usage:**
- Small bot (100 msgs/day): FREE
- Medium bot (10K msgs/day): ~$0.40/month
- Large bot (100K msgs/day): ~$4/month

## If Something Goes Wrong

### Check deployment status:
```bash
gcloud functions describe telegram_webhook --region us-central1
```

### View error logs:
```bash
gcloud functions logs read telegram_webhook --region us-central1 --limit 50
```

### Redeploy with new code:
```bash
./deploy_cloud.sh my-telegram-bot us-central1 "BOT_TOKEN" "API_KEY"
```

### Delete the function:
```bash
gcloud functions delete telegram_webhook --region us-central1
```

## Update Your Bot

### Change the bot code:
1. Edit `main_cloud.py`
2. Re-run the deployment script with same parameters

### Change environment variables:
```bash
gcloud functions deploy telegram_webhook \
  --region us-central1 \
  --update-env-vars TG_BOT_TOKEN=new_token,GEMINI_API_KEY=new_key
```

## Next Steps

✅ **Bot is live!** Your bot is now:
- Running 24/7 on Google Cloud
- Auto-scaling for load
- Monitored and logged
- Backed up automatically

## Need Help?

See **GCF_DEPLOYMENT_GUIDE.md** for detailed setup instructions and troubleshooting.

---

**Happy deploying! 🚀**
