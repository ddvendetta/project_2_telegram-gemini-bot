# 📋 Google Cloud Functions - Command Reference

Quick command reference for Google Cloud Functions deployment and management.

## Pre-Deployment Setup

```bash
# Install Google Cloud SDK
brew install google-cloud-sdk

# Initialize and login
gcloud init
gcloud auth login

# Verify installation
gcloud --version
```

## One-Command Deployment

```bash
./deploy_cloud.sh PROJECT_ID REGION BOT_TOKEN API_KEY
```

**Example:**
```bash
./deploy_cloud.sh my-telegram-bot us-central1 "123456:ABCDEFghijklmnop" "AIzaSyD..."
```

## Manual Deployment (if needed)

### Step 1: Set Project
```bash
gcloud config set project YOUR_PROJECT_ID
```

### Step 2: Enable APIs
```bash
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com
```

### Step 3: Deploy Function
```bash
gcloud functions deploy telegram_webhook \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region us-central1 \
  --entry-point telegram_webhook \
  --set-env-vars TG_BOT_TOKEN=your_token,GEMINI_API_KEY=your_key \
  --source .
```

### Step 4: Get Webhook URL
```bash
gcloud functions describe telegram_webhook \
  --region us-central1 \
  --format='value(httpsTrigger.url)'
```

### Step 5: Set Telegram Webhook
```bash
curl -X POST \
  "https://api.telegram.org/bot$BOT_TOKEN/setWebhook" \
  -d "url=YOUR_FUNCTION_URL"
```

---

## Monitoring & Logs

### View Recent Logs (last 50 entries)
```bash
gcloud functions logs read telegram_webhook --region us-central1 --limit 50
```

### Stream Live Logs
```bash
gcloud functions logs read telegram_webhook --region us-central1 --follow
```

### View Logs from Specific Time
```bash
gcloud functions logs read telegram_webhook --region us-central1 --limit 100
```

### Check Function Status
```bash
gcloud functions describe telegram_webhook --region us-central1
```

---

## Updates & Changes

### Update Environment Variables
```bash
gcloud functions deploy telegram_webhook \
  --region us-central1 \
  --update-env-vars TG_BOT_TOKEN=new_token,GEMINI_API_KEY=new_key
```

### Redeploy with New Code
```bash
# Edit main_cloud.py, then:
gcloud functions deploy telegram_webhook \
  --runtime python312 \
  --trigger-http \
  --region us-central1 \
  --entry-point telegram_webhook \
  --source .
```

### Or use the automated script:
```bash
./deploy_cloud.sh my-telegram-bot us-central1 "NEW_TOKEN" "NEW_KEY"
```

---

## Testing

### Get Current Webhook URL
```bash
gcloud functions describe telegram_webhook \
  --region us-central1 \
  --format='value(httpsTrigger.url)'
```

### Test the Webhook
```bash
curl -X POST \
  "https://your-webhook-url" \
  -H "Content-Type: application/json" \
  -d '{
    "update_id": 123456,
    "message": {
      "message_id": 1,
      "date": 1234567890,
      "chat": {"id": 123, "type": "private"},
      "from": {"id": 123, "is_bot": false, "first_name": "Test"},
      "text": "Test message"
    }
  }'
```

### Test Telegram Webhook Setting
```bash
curl -X POST \
  "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo"
```

---

## Management

### List All Functions
```bash
gcloud functions list --region us-central1
```

### Get Detailed Function Info
```bash
gcloud functions describe telegram_webhook --region us-central1
```

### Check Quotas
```bash
gcloud compute project-info describe --project YOUR_PROJECT_ID
```

---

## Deletion & Cleanup

### Delete the Function
```bash
gcloud functions delete telegram_webhook --region us-central1
```

### Unset Telegram Webhook
```bash
curl -X POST \
  "https://api.telegram.org/bot$BOT_TOKEN/deleteWebhook"
```

### Delete GCP Project (WARNING: Deletes everything!)
```bash
gcloud projects delete YOUR_PROJECT_ID
```

---

## Common Regions

```
us-central1       - USA, Central
us-east1          - USA, East Coast
us-west1          - USA, West Coast
europe-west1      - Europe, Belgium
asia-east1        - Asia, Taiwan
asia-northeast1   - Asia, Tokyo
```

## Useful Environment Variables

Set these before running commands:

```bash
export PROJECT_ID="my-telegram-bot"
export REGION="us-central1"
export TG_BOT_TOKEN="123456:ABCDEFghijklmnop"
export GEMINI_API_KEY="AIzaSyD..."

# Then use in commands:
gcloud functions deploy telegram_webhook \
  --region $REGION \
  --set-env-vars TG_BOT_TOKEN=$TG_BOT_TOKEN,GEMINI_API_KEY=$GEMINI_API_KEY \
  --source .
```

---

## Pricing Reference

**Free tier (always):**
- 2M invocations/month
- 400K GB-seconds/month
- 5GB/month outbound network

**After free tier:**
- $0.40 per 1M invocations
- $0.0000041 per GB-second

**Typical monthly cost:**
- 10K messages: FREE
- 100K messages: ~$0.40
- 1M messages: ~$4

---

## Troubleshooting Commands

### Check if gcloud is working
```bash
gcloud --version
gcloud auth list
gcloud config list
```

### Check project setup
```bash
gcloud projects list
gcloud config get-value project
```

### Check if APIs are enabled
```bash
gcloud services list --enabled
```

### View function creation errors
```bash
gcloud functions logs read telegram_webhook --region us-central1 --limit 100
```

### Check deployment status
```bash
gcloud operations list
gcloud operations describe OPERATION_ID
```

---

## Quick Deploy Script

If the automated script fails, use this manual sequence:

```bash
#!/bin/bash
PROJECT_ID=$1
REGION=$2
TOKEN=$3
API_KEY=$4

gcloud config set project $PROJECT_ID
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com
gcloud functions deploy telegram_webhook \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region $REGION \
  --entry-point telegram_webhook \
  --set-env-vars TG_BOT_TOKEN=$TOKEN,GEMINI_API_KEY=$API_KEY \
  --source . \
  --timeout 60

URL=$(gcloud functions describe telegram_webhook \
  --region $REGION \
  --format='value(httpsTrigger.url)')

echo "Webhook URL: $URL"

curl -X POST \
  "https://api.telegram.org/bot$TOKEN/setWebhook" \
  -d "url=$URL"
```

---

**For more help, see: GCF_DEPLOYMENT_GUIDE.md**
