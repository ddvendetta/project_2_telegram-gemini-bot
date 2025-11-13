# 🚀 Fast Development Cycle - Edit → Deploy → Test on Telegram

**Skip local testing. Deploy directly to GCF and test in Telegram.**

---

## ⚡ Quick Workflow (3 Steps)

### Step 1️⃣ - Edit Your Code
```bash
# Edit the bot code
nano main_cloud.py
# Or use VS Code: code main_cloud.py
```

**What to edit:**
- **Lines 28-37**: System prompt (how bot behaves)
- **Lines 44-80**: Response logic (how bot answers)
- Any other code changes

### Step 2️⃣ - Deploy to GCF (One Command)
```bash
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "8431958486:AAE9WyfhRWSDqXsYXL3ETEekpt5eIEbUEws" "AIzaSyDaRiHiiUMLj_rAH-2y4fzQNFsTA3g0IJE"
```

**What it does:**
- Uploads your code to Google Cloud Functions
- Deploys the changes (takes 2-3 minutes)
- Automatically sets environment variables
- Shows "✅ Deployment successful" when done

### Step 3️⃣ - Test on Telegram
1. Open Telegram app
2. Find your bot
3. Send a message
4. Check if bot responds correctly
5. If yes → done! ✅
6. If no → go back to Step 1️⃣ and edit

---

## 📋 Cheat Sheet

### Deploy Command (Copy & Paste)
```bash
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "8431958486:AAE9WyfhRWSDqXsYXL3ETEekpt5eIEbUEws" "AIzaSyDaRiHiiUMLj_rAH-2y4fzQNFsTA3g0IJE"
```

### Check Deployment Status (While Deploying)
```bash
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
gcloud functions describe telegram_webhook --region asia-southeast1
```

### View Live Logs (To Debug)
```bash
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
gcloud functions logs read telegram_webhook --region asia-southeast1 --follow
```

### Stop Viewing Logs
```bash
Ctrl + C
```

---

## 🎯 Common Changes & How to Make Them

### 1. Change Bot Personality/System Prompt
**File**: `main_cloud.py` (lines 28-37)

```python
SYSTEM_PROMPT = """You are an AI assistant.

Your guidelines:
- Respond in simple terms
- Be friendly and helpful
- Keep responses short"""
```

**Deploy**: `./deploy_cloud.sh ...`

### 2. Add a New Python Package
**File**: `requirements_cloud.txt`

Example - add `requests` package:
```
pyTelegramBotAPI==4.29.1
google-genai>=0.3.0
functions-framework>=3.0.0
requests>=2.31.0
```

**Deploy**: `./deploy_cloud.sh ...`

### 3. Change Model Temperature (Creativity)
**File**: `main_cloud.py` (line 58)

```python
temperature=0.7,  # 0 = factual, 1 = creative
```

**Deploy**: `./deploy_cloud.sh ...`

### 4. Modify Message Handling Logic
**File**: `main_cloud.py` (lines 44-80)

Edit the `get_gemini_response()` function as needed

**Deploy**: `./deploy_cloud.sh ...`

---

## 📊 Development Cycle Timeline

| Step | Time | Action |
|------|------|--------|
| Edit code | 1-5 min | Make changes in `main_cloud.py` |
| Deploy | 2-3 min | Run deploy script |
| Test | 1 min | Send message on Telegram |
| **Total** | **5-9 min per cycle** | From idea to testing |

---

## ✅ Prerequisites (Already Set Up)

You have everything:

- ✅ `main_cloud.py` - Your bot code
- ✅ `requirements_cloud.txt` - Dependencies
- ✅ `deploy_cloud.sh` - Deployment script
- ✅ GCF credentials configured
- ✅ Google Cloud SDK installed
- ✅ Telegram bot token set
- ✅ Gemini API key set

**Nothing else needed!**

---

## 🚨 If Deployment Fails

### Check these things:

```bash
# 1. Verify gcloud is available
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc

# 2. Check syntax errors in your code
python -m py_compile main_cloud.py

# 3. View deployment logs
gcloud functions logs read telegram_webhook --region asia-southeast1 --limit 50

# 4. Check function status
gcloud functions describe telegram_webhook --region asia-southeast1
```

### Common Issues:

| Issue | Solution |
|-------|----------|
| "gcloud: command not found" | Run: `source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc` |
| Syntax error in code | Check `main_cloud.py` for typos |
| Import errors | Add missing package to `requirements_cloud.txt` |
| Bot not responding | Check logs with `gcloud functions logs read...` |
| Deployment timeout | Wait, might just be slow building |

---

## 💡 Pro Tips

1. **Keep edits small** - Change one thing at a time, deploy, test
2. **Watch the logs** - Open logs in another terminal while testing: `gcloud functions logs read telegram_webhook --region asia-southeast1 --follow`
3. **Save your deploy command** - Keep the deploy command handy (maybe in a `.txt` file)
4. **Test edge cases** - Send different types of messages to your bot
5. **Monitor costs** - You're in free tier, but `gcloud functions describe` shows usage

---

## 📝 Your Deployment Command (Save This)

```bash
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "8431958486:AAE9WyfhRWSDqXsYXL3ETEekpt5eIEbUEws" "AIzaSyDaRiHiiUMLj_rAH-2y4fzQNFsTA3g0IJE"
```

Or create a file `deploy.txt` with this command for quick copy-paste.

---

## 🎯 Your Workflow

```
1. Edit main_cloud.py
    ↓
2. Run: ./deploy_cloud.sh ...
    ↓
3. Wait: "✅ Deployment successful"
    ↓
4. Test: Send message on Telegram
    ↓
5. Works? → Done! 🎉
   Doesn't work? → Go to step 1
```

---

## ✨ Summary

You're all set for **rapid iteration**:

- ✅ Edit code (1-5 min)
- ✅ Deploy automatically (2-3 min)
- ✅ Test on Telegram (1 min)
- ✅ Repeat (5-9 min per cycle)

**No local testing needed. No complicated steps. Just edit → deploy → test → repeat.**

---

**Ready to start refining? Edit `main_cloud.py` and deploy! 🚀**
