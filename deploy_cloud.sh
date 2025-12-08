#!/bin/bash

# Google Cloud Functions Deployment Script v2.0
# GCF webhook URL as of 13 Nov 2025 - https://asia-southeast1-gen-lang-client-0715057599.cloudfunctions.net/telegram_webhook 
# Usage: ./deploy_cloud.sh PROJECT_ID REGION [TG_BOT_TOKEN] [GEMINI_API_KEY]
#
# TG_BOT_TOKEN and GEMINI_API_KEY can be provided as arguments or read from .env file.

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to read from .env file
read_env_file() {
    if [ -f ".env" ]; then
        # Read TG_KEY from .env
        TG_BOT_TOKEN=$(grep "^TG_KEY=" .env | cut -d '=' -f2-)
        # Read GEMINI_KEY from .env
        GEMINI_API_KEY=$(grep "^GEMINI_KEY=" .env | cut -d '=' -f2-)
        
        if [ -n "$TG_BOT_TOKEN" ] && [ -n "$GEMINI_API_KEY" ]; then
            echo -e "${BLUE}Credentials read from .env file.${NC}"
            return 0
        fi
    fi
    return 1
}

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: ./deploy_cloud.sh PROJECT_ID REGION [TG_BOT_TOKEN] [GEMINI_API_KEY]"
    echo ""
    echo "Example:"
    echo "  ./deploy_cloud.sh my-telegram-bot us-central1"
    echo "  ./deploy_cloud.sh my-telegram-bot us-central1 123456:ABC-DEF xyz_api_key"
    echo ""
    echo "Parameters:"
    echo "  PROJECT_ID     - Your Google Cloud project ID"
    echo "  REGION         - GCP region (us-central1, us-east1, europe-west1, etc.)"
    echo "  TG_BOT_TOKEN   - (Optional) Your Telegram bot token. If not provided, will read from .env file."
    echo "  GEMINI_API_KEY - (Optional) Your Gemini API key. If not provided, will read from .env file."
    echo ""
    echo "Key Management Best Practice:"
    echo "  Store your credentials in a .env file with:"
    echo "    TG_KEY=your_telegram_bot_token"
    echo "    GEMINI_KEY=your_gemini_api_key"
    echo "  The .env file should NOT be committed to version control."
    exit 1
fi

PROJECT_ID=$1
REGION=$2
FUNCTION_NAME="telegram_webhook"

# Try to read from arguments first, then fall back to .env file
if [ -z "$3" ] || [ -z "$4" ]; then
    if ! read_env_file; then
        echo -e "${RED}Error: Credentials not provided as arguments and .env file not found or incomplete.${NC}"
        echo -e "${RED}Please either:"
        echo -e "${RED}  1. Pass credentials as arguments: ./deploy_cloud.sh PROJECT_ID REGION TG_TOKEN GEMINI_KEY${NC}"
        echo -e "${RED}  2. Create a .env file with TG_KEY and GEMINI_KEY${NC}"
        exit 1
    fi
else
    TG_BOT_TOKEN=$3
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
  --set-env-vars TG_KEY=$TG_BOT_TOKEN,GEMINI_KEY=$GEMINI_API_KEY \
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
