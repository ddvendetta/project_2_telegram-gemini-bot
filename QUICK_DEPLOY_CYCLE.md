# ⚡ Quick Start - Edit & Deploy Cycle

**TL;DR - Just do this:**

```bash
# 1. Edit main_cloud.py in VS Code
# 2. Save the file
# 3. Run this one command:
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"

# 4. Wait 2-3 minutes for "✅ Cloud Function deployed successfully!"
# 5. Test your bot in Telegram
# 6. Repeat!
```

---

## 📝 Edit These Files

### Change How Bot Responds
**File**: `main_cloud.py`  
**Lines**: 28-37

```python
SYSTEM_PROMPT = """Your custom prompt here"""
```

### Add New Packages
**File**: `requirements_cloud.txt`

Add package name, then deploy.

### Change Response Logic
**File**: `main_cloud.py`  
**Function**: `get_gemini_response()` (lines 44-80)

---

## 🚀 Deploy Command

### Full version:
```bash
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"
```

### Make it shorter (add to ~/.zshrc):
```bash
alias deploy-bot='./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"'
```

Then just: `deploy-bot`

---

## 📱 Test Flow

1. Edit code ✏️
2. `./deploy_cloud.sh ...` 🚀 (wait 2-3 min)
3. Open Telegram 💬
4. Send message to bot ➡️
5. Verify response ✅
6. Loop back to step 1 🔄

---

## 🧪 Quick Test Messages

```
"Hello" → Should respond
"What is 2+2?" → Should answer
"Tell a joke" → Should be funny
```

---

## 📊 Timeline

- Edit: 1-5 min ✏️
- Deploy: 2-3 min 🚀
- Test: 1-2 min 💬
- **Total: 5-10 min per cycle** ⏱️

---

## ⚠️ If It Breaks

```bash
# Check logs
gcloud functions logs read telegram_webhook --region asia-southeast1 --limit 50

# Check Python syntax
python -m py_compile main_cloud.py

# Redeploy
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"
```

---

## 📌 Remember

- ✅ Always save `main_cloud.py` before deploying
- ✅ Deploy takes 2-3 minutes
- ✅ Bot is live immediately after deployment
- ✅ Telegram tests show real user experience
- ✅ No local testing needed - deploy and test live
- ✅ Each cycle is only 5-10 minutes

---

**You're ready! Start editing and deploying! 🎉**
