# Deployment Guide for 24/7 Bot

Your Telegram bot can run 24/7 on different platforms. Here are your options:

---

## Option 1: Heroku (Free) - RECOMMENDED FOR BEGINNERS

### Step 1: Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Verify installation
heroku --version
```

### Step 2: Create a Heroku Account
Go to https://www.heroku.com/signup and create a free account.

### Step 3: Login to Heroku
```bash
heroku login
```

### Step 4: Create Procfile
In your project root (`/Users/farhankhairuddin/Project_2`), create a file named `Procfile` (no extension):

```
worker: python main.py
```

### Step 5: Create heroku requirements.txt
Make sure your `requirements.txt` has:
```
pyTelegramBotAPI==4.29.1
google-genai>=0.3.0
```

### Step 6: Initialize Git Repository
```bash
cd /Users/farhankhairuddin/Project_2
git init
git add .
git commit -m "Initial commit"
```

### Step 7: Create Heroku App
```bash
heroku create your-bot-name
```

### Step 8: Set Environment Variables
```bash
heroku config:set TG_BOT_TOKEN="your_telegram_token"
heroku config:set GEMINI_API_KEY="your_gemini_api_key"
```

### Step 9: Deploy
```bash
git push heroku main
```

### Step 10: Verify Deployment
```bash
heroku logs --tail
```

**Pros:** Free, easy to setup, automatic restarts
**Cons:** Free tier has limitations (550 free dyno hours/month)

---

## Option 2: Railway (Recommended) - BEST FREE OPTION

### Step 1: Create Railway Account
Go to https://railway.app and sign up with GitHub

### Step 2: Create Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Connect your GitHub account
- Select your bot repository

### Step 3: Set Environment Variables
In Railway dashboard:
- Go to "Variables"
- Add `TG_BOT_TOKEN`
- Add `GEMINI_API_KEY`

### Step 4: Create Procfile
Create `Procfile` in your project root:
```
worker: python main.py
```

### Step 5: Deploy
Railway automatically deploys when you push to GitHub

**Pros:** Free tier, easy GitHub integration, good uptime
**Cons:** Need GitHub account

---

## Option 3: PythonAnywhere (Best for Python)

### Step 1: Create Account
Go to https://www.pythonanywhere.com and sign up

### Step 2: Upload Files
- Go to "Files" tab
- Create new directory `/yourbot`
- Upload your files:
  - main.py
  - requirements.txt

### Step 3: Create Virtual Environment
In PythonAnywhere console:
```bash
mkvirtualenv --python=/usr/bin/python3.10 botenv
pip install -r requirements.txt
```

### Step 4: Set Environment Variables
Create a `.env` file or set in Web app configuration

### Step 5: Create Web App
- Go to "Web" tab
- Create new web app
- Choose "Python" and your Python version

### Step 6: Configure App
Edit WSGI file to run your bot

**Pros:** Python-focused, good free tier, easy management
**Cons:** Need to configure WSGI differently

---

## Option 4: AWS Lambda + SQS (Serverless)

Perfect for high-volume bots with irregular traffic.

### Step 1: Create AWS Account
Go to https://aws.amazon.com

### Step 2: Create S3 Bucket
Store your code in S3

### Step 3: Create Lambda Function
- Runtime: Python 3.10+
- Handler: main.lambda_handler
- Timeout: 60 seconds

### Step 4: Create SQS Queue
For message queue handling

### Step 5: Deploy
Use AWS CLI:
```bash
aws lambda create-function \
  --function-name telegram-bot \
  --runtime python3.10 \
  --role arn:aws:iam::YOUR_ROLE \
  --handler main.lambda_handler \
  --zip-file fileb://function.zip
```

**Pros:** Serverless, scalable, pay-per-use
**Cons:** More complex, AWS setup required

---

## Option 5: DigitalOcean Droplet (VPS) - BEST FOR CONTROL

### Step 1: Create DigitalOcean Account
Go to https://www.digitalocean.com

### Step 2: Create Droplet
- Choose: Ubuntu 22.04 LTS
- Size: $4/month (Basic)
- Region: Closest to you

### Step 3: SSH into Droplet
```bash
ssh root@your_droplet_ip
```

### Step 4: Install Python & Dependencies
```bash
apt update && apt upgrade -y
apt install -y python3-pip python3-venv git

cd /root
git clone your-bot-repo
cd bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Set Environment Variables
```bash
export TG_BOT_TOKEN="your_token"
export GEMINI_API_KEY="your_key"
```

### Step 6: Run Bot in Background
Option A - Using Screen:
```bash
screen -S bot
python main.py
# Press Ctrl+A then D to detach
```

Option B - Using systemd (Recommended):
Create `/etc/systemd/system/telegram-bot.service`:
```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot
Environment="TG_BOT_TOKEN=your_token"
Environment="GEMINI_API_KEY=your_key"
ExecStart=/root/bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot
systemctl status telegram-bot
```

### Step 7: Monitor
```bash
systemctl logs -u telegram-bot -f
```

**Pros:** Full control, reliable, affordable
**Cons:** Need to manage server

---

## Option 6: Replit (Super Easy)

### Step 1: Create Replit Account
Go to https://replit.com

### Step 2: Import from GitHub
- Click "Import from GitHub"
- Paste your repo URL
- Click Import

### Step 3: Set Secrets
- Click "Secrets" (lock icon)
- Add `TG_BOT_TOKEN`
- Add `GEMINI_API_KEY`

### Step 4: Create Replit.nix
Create `.replit` file:
```
run = "python main.py"
```

### Step 5: Deploy
Click "Run" button - bot starts running

**Pros:** Instant setup, no terminal needed
**Cons:** Limited free tier, less reliable

---

## Comparison Table

| Platform | Cost | Ease | Uptime | Best For |
|---|---|---|---|---|
| **Heroku** | Free/Paid | Easy | Good | Beginners |
| **Railway** | Free/Paid | Easy | Excellent | Easy deployment |
| **PythonAnywhere** | Free/Paid | Medium | Good | Python focus |
| **AWS Lambda** | Pay-per-use | Hard | Excellent | High volume |
| **DigitalOcean** | $4+/month | Medium | Excellent | Full control |
| **Replit** | Free/Paid | Very Easy | Fair | Quick testing |

---

## QUICK START: Railway (Recommended)

The simplest option for 24/7 bot:

### 1. Push to GitHub
```bash
cd /Users/farhankhairuddin/Project_2
git init
git add .
git commit -m "Bot ready"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Create Procfile
```bash
echo "worker: python main.py" > Procfile
git add Procfile
git commit -m "Add Procfile"
git push
```

### 3. Go to Railway.app
- Sign in with GitHub
- New Project → Deploy from GitHub repo
- Select your bot repo
- Add environment variables:
  - `TG_BOT_TOKEN`
  - `GEMINI_API_KEY`

### 4. Done!
Your bot runs 24/7 automatically!

---

## BEST OPTION: DigitalOcean Droplet

If you want full control and reliability:

### 1. Create $4/month Droplet
- Ubuntu 22.04 LTS
- Basic plan
- NYC region (or nearest)

### 2. SSH and Setup (Copy-paste this):
```bash
ssh root@YOUR_IP
apt update && apt upgrade -y
apt install -y python3-pip python3-venv git

cd /root
git clone YOUR_REPO_URL bot
cd bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create Service File:
```bash
cat > /etc/systemd/system/telegram-bot.service << EOF
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/bot
Environment="TG_BOT_TOKEN=YOUR_TOKEN"
Environment="GEMINI_API_KEY=YOUR_KEY"
ExecStart=/root/bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### 4. Start Service:
```bash
systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot
systemctl status telegram-bot
```

### 5. Monitor Logs:
```bash
systemctl logs -u telegram-bot -f
```

That's it! Bot runs 24/7 with auto-restart on failure.

---

## Testing Your Deployment

After deploying:

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Send a test message
5. Check logs for errors

---

## Troubleshooting

### Bot not responding
```bash
# Check logs
heroku logs --tail          # Heroku
railway logs                # Railway
systemctl logs -u telegram-bot -f  # DigitalOcean
```

### Environment variables not set
```bash
# Verify they're set
heroku config               # Heroku
railway variables           # Railway
echo $TG_BOT_TOKEN         # Check locally
```

### Bot keeps crashing
- Check error logs
- Ensure all packages installed
- Verify API keys are correct
- Add error handling

---

## My Recommendation

**For You (Easiest):** Railway.app
- Sign in with GitHub
- Connect your repo
- Add environment variables
- Done! 24/7 bot running

**For Production:** DigitalOcean Droplet
- Full control
- Reliable
- Only $4/month
- Auto-restart on crash
- Easy to monitor

---

## Files You Need

Make sure these are in your project:
- ✅ `main.py` (your bot code)
- ✅ `requirements.txt` (dependencies)
- ✅ `Procfile` (for most platforms) - see above
- ✅ `.env` file (for local testing only - DON'T push to Git)

---

## Next Steps

1. Choose a platform (I recommend Railway)
2. Follow the setup steps
3. Push your code
4. Set environment variables
5. Deploy!
6. Test your bot

Your bot will now run 24/7! 🎉

---

## Need Help?

- **Railway**: https://docs.railway.app
- **Heroku**: https://devcenter.heroku.com
- **DigitalOcean**: https://docs.digitalocean.com
- **PythonAnywhere**: https://help.pythonanywhere.com

Good luck! 🚀
