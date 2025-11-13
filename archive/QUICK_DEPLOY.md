# ⚡ 5-Minute Deployment Guide

Get your bot running 24/7 in 5 minutes!

## FASTEST: Railway.app

### 1. Prepare GitHub (2 min)
```bash
cd /Users/farhankhairuddin/Project_2
git init
git add .
git commit -m "Bot ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy on Railway (2 min)
- Go to https://railway.app
- Click "New Project"
- Select "Deploy from GitHub repo"
- Authorize GitHub
- Select your repository
- Click Deploy

### 3. Add Secrets (1 min)
In Railway dashboard:
- Click "Variables"
- Add: `TG_BOT_TOKEN` = your telegram token
- Add: `GEMINI_API_KEY` = your gemini key

**Done!** Your bot now runs 24/7! ✅

---

## ALTERNATIVE: Heroku (3 min)

```bash
# 1. Install Heroku CLI
brew tap heroku/brew && brew install heroku

# 2. Login
heroku login

# 3. Create app
heroku create your-bot-name

# 4. Set environment
heroku config:set TG_BOT_TOKEN="your_token"
heroku config:set GEMINI_API_KEY="your_key"

# 5. Deploy
git push heroku main

# 6. Check if running
heroku logs --tail
```

**Done!** Your bot runs 24/7! ✅

---

## ALTERNATIVE: DigitalOcean VPS (10 min)

### 1. Create Droplet
- Go to https://digitalocean.com
- Click "Create" → "Droplets"
- Choose Ubuntu 22.04 LTS, $4/month
- Create

### 2. Connect & Setup
```bash
# SSH into your droplet
ssh root@YOUR_DROPLET_IP

# Copy-paste this entire block:
apt update && apt upgrade -y
apt install -y python3-pip python3-venv git

cd /root
git clone YOUR_REPO_URL bot
cd bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create Service File
```bash
# Copy this:
cat > /etc/systemd/system/telegram-bot.service << 'EOF'
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot
Environment="TG_BOT_TOKEN=YOUR_TOKEN_HERE"
Environment="GEMINI_API_KEY=YOUR_KEY_HERE"
ExecStart=/root/bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

Replace YOUR_TOKEN_HERE and YOUR_KEY_HERE with actual values!

### 4. Start Service
```bash
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot
systemctl status telegram-bot
```

**Done!** Your bot runs 24/7 with auto-restart! ✅

---

## Which Should I Use?

| Platform | Time | Cost | Reliability | Recommended |
|----------|------|------|-------------|---|
| Railway | 5 min | Free/Paid | ⭐⭐⭐⭐⭐ | ✅ YES |
| Heroku | 5 min | Free/Paid | ⭐⭐⭐⭐ | ✅ YES |
| DigitalOcean | 10 min | $4/mo | ⭐⭐⭐⭐⭐ | ✅ BEST |

---

## Verify Deployment

After deploying:

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Send a test message
5. Should get a response ✅

If no response:
- Check environment variables are set
- Check logs for errors:
  - Railway: Click "Logs" tab
  - Heroku: Run `heroku logs --tail`
  - DigitalOcean: Run `systemctl logs -u telegram-bot -f`

---

## Common Issues

### Bot doesn't respond
✓ Check environment variables
✓ Check bot token is correct
✓ Check API key is correct
✓ Check internet connection

### Environment variables not working
- Make sure they're set in the platform
- Don't push `.env` files to Git
- Restart the bot after setting variables

### Bot crashes on startup
- Check `main.py` for errors
- Check all required packages installed
- Check API keys are valid

---

## Monitor Your Bot

### Railway
- Dashboard shows logs automatically
- Click "Logs" to see real-time output

### Heroku
```bash
heroku logs --tail
```

### DigitalOcean
```bash
ssh root@YOUR_IP
systemctl logs -u telegram-bot -f
```

---

## Stop/Restart Bot

### Railway
- Click "Pause Deployment" or delete

### Heroku
```bash
heroku restart
heroku ps:stop web
```

### DigitalOcean
```bash
systemctl restart telegram-bot
systemctl stop telegram-bot
systemctl status telegram-bot
```

---

## Update Bot Code

### Railway / Heroku
```bash
git add .
git commit -m "Update bot"
git push origin main  # Railway auto-deploys
git push heroku main  # For Heroku
```

### DigitalOcean
```bash
ssh root@YOUR_IP
cd /root/bot
git pull
systemctl restart telegram-bot
```

---

## Cost Breakdown

- **Railway Free**: Up to 500 hours/month (enough for one bot)
- **Heroku Free**: Ended, now $7+/month
- **DigitalOcean**: $4/month for basic VPS
- **AWS Lambda**: Pay per request (~free for low traffic)

**Recommendation**: Railway (free and reliable) or DigitalOcean ($4/month for full control)

---

## Done! 🎉

Your bot now runs 24/7! 

Need help? Check `DEPLOYMENT_GUIDE.md` for detailed instructions.
