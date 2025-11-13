# ✅ Pre-Deployment Checklist

Complete this checklist before deploying your bot:

## Code Preparation

- [ ] `main.py` works locally
  ```bash
  export TG_BOT_TOKEN="your_token"
  export GEMINI_API_KEY="your_key"
  python main.py
  ```

- [ ] `requirements.txt` is complete
  ```bash
  pip freeze > requirements.txt
  ```

- [ ] No hardcoded tokens or keys in code
  ```bash
  grep -r "TG_BOT_TOKEN\|GEMINI_API_KEY" main.py  # Should be empty or env only
  ```

- [ ] Bot responds correctly to test messages

## Git Setup

- [ ] Git repository initialized
  ```bash
  git init
  ```

- [ ] `.gitignore` created and includes:
  - [ ] `.env` or environment files
  - [ ] `GEM_KEY`, `TG_KEY` files
  - [ ] `__pycache__/`, `*.pyc`
  - [ ] `venv/`, `.venv/`

- [ ] All necessary files added
  ```bash
  git add .
  git status  # Review files
  ```

- [ ] Initial commit made
  ```bash
  git commit -m "Initial bot commit"
  ```

- [ ] GitHub repository created
  - [ ] Visit github.com and create new repo
  - [ ] Follow the "push existing repo" instructions

## Telegram Setup

- [ ] You have a Telegram bot token from @BotFather
  - [ ] Token starts with numbers
  - [ ] Stored safely (not in code)

- [ ] Bot is named appropriately
  - [ ] Username set in @BotFather
  - [ ] Description set in @BotFather

## Gemini Setup

- [ ] You have a Gemini API key
  - [ ] From Google AI Studio or Google Cloud
  - [ ] Has proper permissions
  - [ ] Not expired

## Platform Selection

- [ ] Choose deployment platform:
  - [ ] Railway (⭐ Recommended)
  - [ ] Heroku
  - [ ] DigitalOcean VPS
  - [ ] PythonAnywhere
  - [ ] Other: _________

## Pre-Deployment Files

- [ ] `Procfile` exists (for Railway/Heroku)
- [ ] `telegram-bot.service` exists (for Linux VPS)
- [ ] `README.md` updated with instructions
- [ ] `QUICK_DEPLOY.md` or `DEPLOYMENT_GUIDE.md` reviewed

## Deployment (Choose Your Platform)

### Railway Deployment

- [ ] Created railway.app account
- [ ] GitHub account connected to Railway
- [ ] Repository pushed to GitHub
- [ ] Railway project created from GitHub
- [ ] Environment variables added in Railway:
  - [ ] `TG_BOT_TOKEN`
  - [ ] `GEMINI_API_KEY`
- [ ] Deployment shows "Running" status
- [ ] Logs show "Bot is running..."

### Heroku Deployment

- [ ] Heroku account created
- [ ] Heroku CLI installed
- [ ] `heroku login` completed
- [ ] Heroku app created
- [ ] Environment variables set via `heroku config:set`
- [ ] Repository pushed to heroku
- [ ] `heroku logs --tail` shows "Bot is running..."

### DigitalOcean Deployment

- [ ] Droplet created (Ubuntu 22.04 LTS, $4/month)
- [ ] SSH access working
- [ ] Python3 and pip installed
- [ ] Virtual environment created
- [ ] Requirements installed
- [ ] Systemd service file copied
- [ ] Environment variables set in service file
- [ ] Service enabled and started
- [ ] `systemctl status telegram-bot` shows "running"

## Post-Deployment Verification

- [ ] Bot runs without errors
- [ ] Message response is immediate
- [ ] No errors in logs
- [ ] Bot continues running after 5 minutes

### Test Messages to Send

1. `/start` → Should get welcome message
2. `Hello` → Should get AI response
3. `What is 2+2?` → Should get answer
4. Long question → Should be split properly if needed

## Monitoring Setup

- [ ] Know how to check logs
  - [ ] Railway: Dashboard → Logs
  - [ ] Heroku: `heroku logs --tail`
  - [ ] DigitalOcean: `systemctl logs -u telegram-bot -f`

- [ ] Know how to restart bot
  - [ ] Railway: Pause/Resume in dashboard
  - [ ] Heroku: `heroku restart`
  - [ ] DigitalOcean: `systemctl restart telegram-bot`

- [ ] Know how to update code
  - [ ] Git push to main branch
  - [ ] Platform auto-redeploys (Railway)
  - [ ] Or manually restart if needed

## Troubleshooting Prepared

- [ ] I understand that without response = check logs
- [ ] I know to verify environment variables first
- [ ] I know how to restart the bot
- [ ] I have the token/key backed up safely

## Final Checks

- [ ] Bot works locally: ✅
- [ ] Code is in GitHub: ✅
- [ ] Tokens are in platform (not Git): ✅
- [ ] Deployment succeeds: ✅
- [ ] Bot responds in Telegram: ✅

---

## You're Ready! 🎉

If all checkboxes are ✅, your bot is deployed and running 24/7!

### Deployment Complete?

Then you're done! Your bot:
- ✅ Runs 24/7 automatically
- ✅ Restarts on failure (most platforms)
- ✅ Responds to all messages
- ✅ Handles long messages properly
- ✅ Uses your custom system prompt

### Something Not Working?

1. Check `DEPLOYMENT_GUIDE.md` for your platform
2. Review logs for error messages
3. Verify environment variables are set correctly
4. Make sure bot token and API key are valid
5. Test locally first before debugging deployment

---

**Questions?** See the detailed guides:
- `QUICK_DEPLOY.md` - 5-minute guide
- `DEPLOYMENT_GUIDE.md` - Complete instructions
- `DEPLOYMENT_READY.md` - Status and summary

**You've got this!** 🚀
