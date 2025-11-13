# ✅ Google Cloud Functions - Pre-Deployment Checklist

Complete this checklist before deploying your bot to Google Cloud Functions.

## 📋 Prerequisites

- [ ] Have a Google account (free)
- [ ] Have a Telegram bot token from @BotFather
- [ ] Have a Gemini API key from [ai.google.dev](https://ai.google.dev)
- [ ] Terminal/Command line access
- [ ] 15 minutes of time

## 💻 Machine Setup

- [ ] Google Cloud SDK installed
  ```bash
  brew install google-cloud-sdk
  ```

- [ ] Google Cloud SDK initialized
  ```bash
  gcloud init
  gcloud auth login
  ```

- [ ] Can run gcloud commands
  ```bash
  gcloud --version  # Should show version info
  ```

## 📝 Credentials Ready

- [ ] Telegram Bot Token (format: `123456:ABCDEFghijklmnop`)
- [ ] Gemini API Key (starts with `AIzaSy...`)
- [ ] Decided on GCP Project ID (e.g., `my-telegram-bot`)
- [ ] Decided on Region (default: `us-central1`)

## 📁 Project Files

- [ ] `main_cloud.py` exists (webhook-based bot code)
- [ ] `requirements_cloud.txt` exists (dependencies)
- [ ] `deploy_cloud.sh` exists and is executable
  ```bash
  chmod +x deploy_cloud.sh
  ls -la deploy_cloud.sh  # Should show -rwxr-xr-x
  ```

## 📖 Documentation Review

- [ ] Read `GCF_READY_TO_DEPLOY.md` (overview)
- [ ] Read `QUICK_GCF_DEPLOY.md` (quick 5-min guide)
- [ ] Bookmarked `GCF_COMMANDS_REFERENCE.md` (commands cheat sheet)
- [ ] Have `GCF_DEPLOYMENT_GUIDE.md` available (detailed guide)

## 🚀 Ready to Deploy

### Quick Start (Recommended)

```bash
# 1. Run the automated deployment script
./deploy_cloud.sh my-telegram-bot us-central1 "YOUR_BOT_TOKEN" "YOUR_API_KEY"

# 2. Wait 2-3 minutes
# 3. See "✅ Cloud Function deployed successfully!"
# 4. Test in Telegram
```

### Manual Deployment (if script doesn't work)

```bash
# 1. Set project
gcloud config set project my-telegram-bot

# 2. Enable APIs
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com

# 3. Deploy function
gcloud functions deploy telegram_webhook \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --entry-point telegram_webhook \
  --set-env-vars TG_BOT_TOKEN=YOUR_TOKEN,GEMINI_API_KEY=YOUR_KEY \
  --source . \
  --timeout 60

# 4. Get webhook URL
gcloud functions describe telegram_webhook \
  --region us-central1 \
  --format='value(httpsTrigger.url)'

# 5. Set Telegram webhook (replace YOUR_URL with output from step 4)
curl -X POST \
  "https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook" \
  -d "url=YOUR_URL"
```

## ✔️ Deployment Success Criteria

After deployment, verify these:

- [ ] Deployment script shows `✅ Cloud Function deployed successfully!`
- [ ] Got a webhook URL (looks like `https://us-central1-...cloudfunctions.net/...`)
- [ ] Script shows `✅ Telegram webhook set successfully!`
- [ ] No error messages in output

## 🧪 Testing the Bot

After successful deployment:

- [ ] Open Telegram app
- [ ] Find your bot
- [ ] Send a test message (e.g., "Hello")
- [ ] Bot responds with AI response in 1-5 seconds
- [ ] Send another message to verify it works

**If no response:**
1. Wait 30 seconds (function might be cold-starting)
2. Check logs: `gcloud functions logs read telegram_webhook --region us-central1 --limit 20`
3. See troubleshooting section below

## 📊 Monitoring Setup

- [ ] Know how to check logs
  ```bash
  gcloud functions logs read telegram_webhook --region us-central1 --follow
  ```

- [ ] Know how to check function status
  ```bash
  gcloud functions describe telegram_webhook --region us-central1
  ```

## 🎯 Optional Enhancements

After deployment is working:

- [ ] Customize system prompt in `main_cloud.py` (line 28-37)
- [ ] Test with different message types
- [ ] Monitor logs for first few hours
- [ ] Add to contacts in Telegram
- [ ] Test with multiple users

## 🛟 Troubleshooting

### "deployment timeout"
- **Solution:** Rerun deploy script or manual commands

### "gcloud: command not found"
- **Solution:** Install Google Cloud SDK
  ```bash
  brew install google-cloud-sdk
  gcloud init
  ```

### "Project not found"
- **Solution:** 
  1. Make sure project ID exists: `gcloud projects list`
  2. Or create new project in Google Cloud Console
  3. Make sure you've run `gcloud auth login`

### "Bot not responding in Telegram"
- **Check:** 
  ```bash
  # View logs for errors
  gcloud functions logs read telegram_webhook --region us-central1 --limit 50
  
  # Check if webhook was set
  curl -X POST "https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo"
  ```

### "DEADLINE_EXCEEDED"
- **Cause:** Function timeout
- **Solution:** Edit `main_cloud.py` to make responses faster, or increase timeout in gcloud deploy command

### "permission denied"
- **Solution:** Make sure you've authenticated
  ```bash
  gcloud auth login
  gcloud auth application-default login
  ```

## 📞 Getting Help

- **Quick commands:** See `GCF_COMMANDS_REFERENCE.md`
- **Detailed guide:** See `GCF_DEPLOYMENT_GUIDE.md`
- **5-minute guide:** See `QUICK_GCF_DEPLOY.md`
- **Logs:** `gcloud functions logs read telegram_webhook --region us-central1 --follow`

## ⏱️ Timeline

- **2-3 minutes:** Deployment time
- **30 seconds:** Function activation (cold start)
- **1-5 seconds:** Response time per message
- **Hours:** Google Cloud logs retention (7 days by default)

## 💰 Costs

**You will NOT be charged if:**
- Using less than 2M invocations/month
- Using less than 400K GB-seconds/month

**Typical bot usage:**
- 100 msgs/day: FREE ✅
- 1000 msgs/day: FREE ✅
- 10K msgs/day: ~$0.40/month
- 100K msgs/day: ~$4/month

## 🎉 Success!

Once your bot is live:

1. ✅ Bot runs 24/7 on Google Cloud
2. ✅ Automatically scales for load
3. ✅ Costs almost nothing
4. ✅ No servers to manage
5. ✅ Can redeploy anytime

**Now enjoy your always-on Telegram bot! 🚀**

---

## Quick Reference Commands

```bash
# Deploy (automated)
./deploy_cloud.sh my-telegram-bot us-central1 "BOT_TOKEN" "API_KEY"

# Check status
gcloud functions describe telegram_webhook --region us-central1

# View logs
gcloud functions logs read telegram_webhook --region us-central1 --follow

# Update code and redeploy
./deploy_cloud.sh my-telegram-bot us-central1 "BOT_TOKEN" "API_KEY"

# Delete function
gcloud functions delete telegram_webhook --region us-central1
```

---

**Ready? Run: `./deploy_cloud.sh` 🚀**
