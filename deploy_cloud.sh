#!/bin/bash

# Google Cloud Functions Deployment Script v1.0
# GCF webhook URL as of 13 Nov 2025 - https://asia-southeast1-gen-lang-client-0715057599.cloudfunctions.net/telegram_webhook 
# Usage: ./deploy_cloud.sh PROJECT_ID REGION [TG_BOT_TOKEN] [GEMINI_API_KEY]
#
# TG_BOT_TOKEN and GEMINI_API_KEY can be provided as arguments or read from TG_KEY and GEM_KEY files.

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: ./deploy_cloud.sh PROJECT_ID REGION [TG_BOT_TOKEN] [GEMINI_API_KEY]"
    echo ""
    echo "Example:"
    echo "  ./deploy_cloud.sh my-telegram-bot us-central1"
    echo "  ./deploy_cloud.sh my-telegram-bot us-central1 123456:ABC-DEF xyz_api_key"
    echo ""
    echo "Parameters:"
    echo "  PROJECT_ID    - Your Google Cloud project ID"
    echo "  REGION        - GCP region (us-central1, us-east1, europe-west1, etc.)"
    echo "  TG_BOT_TOKEN  - (Optional) Your Telegram bot token from @BotFather. If not provided, will try to read from TG_KEY file."
    echo "  GEMINI_API_KEY - (Optional) Your Gemini API key from Google AI Studio. If not provided, will try to read from GEM_KEY file."
    echo ""
    echo "Key Management Best Practice:"
    echo "  Store your TG_BOT_TOKEN in a file named 'TG_KEY' and GEMINI_API_KEY in a file named 'GEM_KEY' in the same directory as this script."
    echo "  Ensure these files are not committed to version control (e.g., add them to .gitignore)."
    exit 1
fi

PROJECT_ID=$1
REGION=$2
FUNCTION_NAME="telegram_webhook"

# Try to read TG_BOT_TOKEN from file if not provided as argument
if [ -z "$3" ]; then
    if [ -f "TG_KEY" ]; then
        TG_BOT_TOKEN=$(head -n 1 TG_KEY)
        echo -e "${BLUE}TG_BOT_TOKEN read from TG_KEY file.${NC}"
    else
        echo -e "${RED}Error: TG_BOT_TOKEN not provided and TG_KEY file not found.${NC}"
        exit 1
    fi
else
    TG_BOT_TOKEN=$3
fi

# Try to read GEMINI_API_KEY from file if not provided as argument
if [ -z "$4" ]; then
    if [ -f "GEM_KEY" ]; then
        GEMINI_API_KEY=$(head -n 1 GEM_KEY)
        echo -e "${BLUE}GEMINI_API_KEY read from GEM_KEY file.${NC}"
    else
        echo -e "${RED}Error: GEMINI_API_KEY not provided and GEM_KEY file not found.${NC}"
        exit 1
    fi
else
    GEMINI_API_KEY=$4
fi

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Google Cloud Functions Deployment${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo "Configuration:"
echo "  Project ID:  $PROJECT_ID"
echo "  Region:      $REGION"
echo "  Function:    $FUNCTION_NAME"
echo ""

# Step 1: Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI not found. Please install it first.${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Step 2: Set project
echo -e "${BLUE}Setting Google Cloud project...${NC}"
gcloud config set project $PROJECT_ID

# Step 3: Enable APIs
echo -e "${BLUE}Enabling required APIs...${NC}"
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Step 4: Deploy function
echo -e "${BLUE}Deploying Cloud Function (this takes 2-3 minutes)...${NC}"
gcloud functions deploy $FUNCTION_NAME \
  --runtime python312 \
  --trigger-http \
  --allow-unauthenticated \
  --region $REGION \
  --entry-point telegram_webhook \
  --source . \
  --set-env-vars TG_BOT_TOKEN=$TG_BOT_TOKEN,GEMINI_API_KEY=$GEMINI_API_KEY \
  --timeout 60

# Step 5: Get webhook URL
echo -e "${BLUE}Getting webhook URL...${NC}"
WEBHOOK_URL=$(gcloud functions describe $FUNCTION_NAME \
  --region $REGION \
  --format='value(serviceConfig.uri)')

echo ""
echo -e "${GREEN}✅ Cloud Function deployed successfully!${NC}"
echo ""
echo "Webhook URL:"
echo "  $WEBHOOK_URL"
echo ""

# Step 6: Set Telegram webhook
echo -e "${BLUE}Setting Telegram webhook...${NC}"
WEBHOOK_RESPONSE=$(curl -s -X POST \
  "https://api.telegram.org/bot$TG_BOT_TOKEN/setWebhook" \
  -d "url=$WEBHOOK_URL")

echo ""
if echo $WEBHOOK_RESPONSE | grep -q '"ok":true'; then
    echo -e "${GREEN}✅ Telegram webhook set successfully!${NC}"
else
    echo -e "${RED}⚠️  Warning: Webhook setting response:${NC}"
    echo "$WEBHOOK_RESPONSE"
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""
echo "Your bot is now live on Google Cloud Functions!"
echo ""
echo "Test your bot:"
echo "  1. Open Telegram"
echo "  2. Find your bot"
echo "  3. Send a test message"
echo "  4. Should get a response"
echo ""
echo "Monitor logs:"
echo "  gcloud functions logs read $FUNCTION_NAME --region $REGION --follow"
echo ""
echo "Delete the function (if needed):"
echo "  gcloud functions delete $FUNCTION_NAME --region $REGION"
echo ""
