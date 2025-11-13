# Project Structure - Essential Files Only

## 📂 Current Directory Structure

```
Project_2/
├── 🚀 PRODUCTION FILES
│   ├── main.py                    (Local/VPS polling version)
│   ├── main_cloud.py              (Google Cloud Functions webhook version)
│   ├── requirements.txt           (Standard dependencies)
│   └── requirements_cloud.txt     (Cloud Functions dependencies)
│
├── 🔐 CREDENTIALS
│   ├── GEM_KEY                    (Gemini API key)
│   └── TG_KEY                     (Telegram bot token)
│
├── 📖 DOCUMENTATION
│   ├── README.md                  (Project overview)
│   ├── MASTER_GCF_GUIDE.md        (Complete GCF deployment guide)
│   └── GCF_COMMANDS_REFERENCE.md  (Command cheat sheet)
│
├── 🚀 DEPLOYMENT
│   └── deploy_cloud.sh            (Automated GCF deployment script)
│
├── 📦 ENVIRONMENT
│   ├── venv/                      (Python virtual environment)
│   └── __pycache__/               (Python cache)
│
└── 📦 ARCHIVE (legacy/redundant files)
    └── archive/                   (29 archived files)
```

---

## ✅ Essential Production Files

### Application Code
- **`main.py`** (4.0K) - Polling-based bot for local testing and VPS deployment
- **`main_cloud.py`** (4.0K) - Webhook-based bot for Google Cloud Functions

### Dependencies
- **`requirements.txt`** - Standard dependencies (pyTelegramBotAPI, google-genai)
- **`requirements_cloud.txt`** - GCF dependencies (adds functions-framework)

### Credentials
- **`GEM_KEY`** - Your Gemini API key (39 bytes)
- **`TG_KEY`** - Your Telegram bot token (48 bytes)

### Deployment
- **`deploy_cloud.sh`** (3.5K) - One-command deployment script for GCF

### Documentation
- **`README.md`** - Project overview
- **`MASTER_GCF_GUIDE.md`** (9.5K) - Complete deployment guide
- **`GCF_COMMANDS_REFERENCE.md`** (5.8K) - Command reference

---

## 📦 What Was Archived

**29 files moved to `archive/` folder:**

- Redundant documentation guides (16 files)
- Duplicate code files (4 files)
- Alternative deployment scripts (5 files)
- Service configuration files (2 files)
- Other configuration files (2 files)

**Examples of archived files:**
- `DEPLOYMENT_COMPLETE.md`
- `GCF_DEPLOYMENT_GUIDE.md`
- `START_HERE.md`
- `cloud_functions.py`
- `main_polling.py`
- `Procfile` (Heroku/Railway)
- `telegram-bot.service` (VPS systemd)
- `deploy.sh` (alternative deployment)

---

## 🎯 Quick Reference for Development

### Run Locally (Testing)
```bash
source venv/bin/activate
export TG_BOT_TOKEN="your_token"
export GEMINI_API_KEY="your_key"
python main.py
```

### Deploy to Google Cloud Functions
```bash
./deploy_cloud.sh your-project asia-southeast1 "YOUR_TOKEN" "YOUR_KEY"
```

### Check GCF Status
```bash
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
gcloud functions describe telegram_webhook --region asia-southeast1
gcloud functions logs read telegram_webhook --region asia-southeast1 --follow
```

---

## 📝 For Refinements & Updates

To make changes to your application:

1. **Edit bot logic**: Modify `main_cloud.py` (lines 28-37 for system prompt)
2. **Update dependencies**: Edit `requirements_cloud.txt` and add packages
3. **Deploy changes**: Run `./deploy_cloud.sh`
4. **Test locally**: Use `main.py` with polling

---

## 🔄 File Organization Summary

| Type | Files | Location |
|------|-------|----------|
| Application Code | 2 | Root (`.py`) |
| Dependencies | 2 | Root (`.txt`) |
| Deployment Script | 1 | Root (`.sh`) |
| Credentials | 2 | Root (key files) |
| Documentation | 3 | Root (`.md`) |
| Python Environment | 1 | `venv/` |
| Legacy Files | 29 | `archive/` |

---

**Your project is now clean and organized for active development! 🎉**

All essential files for the GCF deployment and continued refinement are in the root directory.
Archived files are safely stored in the `archive/` subfolder if you need them later.
