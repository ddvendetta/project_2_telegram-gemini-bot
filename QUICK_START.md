# 🚀 QUICK REFERENCE - Edit → Deploy → Test

## Your 3-Step Development Cycle

### 1️⃣ EDIT CODE
```bash
nano main_cloud.py        # Or: code main_cloud.py
```
Change lines 28-37 (system prompt) or any code logic

---

### 2️⃣ DEPLOY TO GCF
```bash
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "8431958486:AAE9WyfhRWSDqXsYXL3ETEekpt5eIEbUEws" "AIzaSyDaRiHiiUMLj_rAH-2y4fzQNFsTA3g0IJE"
```
Wait for: `✅ Deployment successful`

---

### 3️⃣ TEST ON TELEGRAM
- Open Telegram
- Send message to bot
- Check response
- ✅ Done or repeat

---

## ⏱️ Timing
| Step | Time |
|------|------|
| Edit | 1-5 min |
| Deploy | 2-3 min |
| Test | 1 min |
| **Total** | **5-9 min** |

---

## 🔧 Common Edits

### Change Bot Behavior
**File**: `main_cloud.py` lines 28-37
```python
SYSTEM_PROMPT = """You are...
Your guidelines:
- ...
"""
```

### Add Package
**File**: `requirements_cloud.txt`
```
pyTelegramBotAPI==4.29.1
google-genai>=0.3.0
functions-framework>=3.0.0
requests>=2.31.0        # ← Add new packages
```

### Change Creativity
**File**: `main_cloud.py` line 58
```python
temperature=0.7,  # 0=factual, 1=creative
```

---

## 🐛 Debugging

### View Live Logs
```bash
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
gcloud functions logs read telegram_webhook --region asia-southeast1 --follow
```

### Check Syntax
```bash
python -m py_compile main_cloud.py
```

### Check Status
```bash
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
gcloud functions describe telegram_webhook --region asia-southeast1
```

---

## 📋 Files You Have
- ✅ `main_cloud.py` - Bot code (edit this)
- ✅ `requirements_cloud.txt` - Packages
- ✅ `deploy_cloud.sh` - Deploy script (run this)
- ✅ GCF credentials - Already set
- ✅ Telegram token - Ready
- ✅ Gemini API key - Ready

**Everything ready to go! 🎉**

---

**Start here**: `nano main_cloud.py` → Edit → `./deploy_cloud.sh ...` → Test on Telegram
