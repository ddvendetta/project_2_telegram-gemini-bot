# 🔧 Deploy Script Fixed

## The Problem
After every deployment, the webhook URL wasn't being set automatically. You had to manually run:
```bash
curl -X POST "https://api.telegram.org/bot{TOKEN}/setWebhook" -d "url={URL}"
```

## The Root Cause
The deploy script was trying to get the webhook URL using the **Gen 1 Cloud Functions format**:
```bash
httpsTrigger.url  # ❌ WRONG - for Gen 1 functions
```

But your bot uses **Gen 2 Cloud Functions**, which uses:
```bash
serviceConfig.uri  # ✅ CORRECT - for Gen 2 functions
```

## The Fix
Updated `deploy_cloud.sh` line 76:

**Before:**
```bash
WEBHOOK_URL=$(gcloud functions describe $FUNCTION_NAME \
  --region $REGION \
  --format='value(httpsTrigger.url)')
```

**After:**
```bash
WEBHOOK_URL=$(gcloud functions describe $FUNCTION_NAME \
  --region $REGION \
  --format='value(serviceConfig.uri)')
```

## Now What?
✅ **Every deployment automatically:**
1. Deploys the code
2. Gets the correct webhook URL
3. Sets it in Telegram
4. Confirms success

**You no longer need to manually set the webhook!**

## Next Deployment
Just run:
```bash
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"
```

The webhook will be set automatically at the end. ✅

---

**Updated**: 2025-11-12  
**Status**: Ready for hassle-free deployments
