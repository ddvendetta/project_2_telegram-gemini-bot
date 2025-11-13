#!/bin/bash
# Quick deployment script for Railway, Heroku, or DigitalOcean
# Usage: ./deploy.sh

set -e

echo "🚀 Telegram Bot Deployment Helper"
echo "=================================="
echo ""
echo "Choose your deployment platform:"
echo "1) Railway (Recommended - easiest)"
echo "2) Heroku"
echo "3) DigitalOcean VPS"
echo "4) PythonAnywhere"
echo ""

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📱 Railway Deployment"
        echo "===================="
        echo ""
        echo "Step 1: Create Procfile ✓ (Already done)"
        echo "Step 2: Push to GitHub:"
        echo "  git init"
        echo "  git add ."
        echo "  git commit -m 'Bot ready'"
        echo "  git push origin main"
        echo ""
        echo "Step 3: Go to https://railway.app"
        echo "Step 4: New Project → Deploy from GitHub"
        echo "Step 5: Add variables:"
        echo "  - TG_BOT_TOKEN"
        echo "  - GEMINI_API_KEY"
        echo ""
        echo "✅ Done! Your bot runs 24/7"
        ;;
    
    2)
        echo ""
        echo "🔶 Heroku Deployment"
        echo "===================="
        echo ""
        echo "Step 1: Install Heroku CLI"
        echo "  brew tap heroku/brew && brew install heroku"
        echo ""
        echo "Step 2: Login"
        echo "  heroku login"
        echo ""
        echo "Step 3: Create app"
        echo "  heroku create your-bot-name"
        echo ""
        echo "Step 4: Set environment variables"
        echo "  heroku config:set TG_BOT_TOKEN='your_token'"
        echo "  heroku config:set GEMINI_API_KEY='your_key'"
        echo ""
        echo "Step 5: Deploy"
        echo "  git push heroku main"
        echo ""
        echo "Step 6: Check logs"
        echo "  heroku logs --tail"
        ;;
    
    3)
        echo ""
        echo "🖥️  DigitalOcean VPS Deployment"
        echo "==============================="
        echo ""
        echo "Step 1: Create Ubuntu 22.04 Droplet ($4/month)"
        echo "  - Go to digitalocean.com"
        echo "  - Create Droplet"
        echo "  - Choose Ubuntu 22.04 LTS"
        echo ""
        echo "Step 2: SSH into droplet"
        echo "  ssh root@YOUR_DROPLET_IP"
        echo ""
        echo "Step 3: Run these commands:"
        echo ""
        cat << 'SETUP'
apt update && apt upgrade -y
apt install -y python3-pip python3-venv git

cd /root
git clone YOUR_REPO_URL bot
cd bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cat > /etc/systemd/system/telegram-bot.service << 'SERVICE'
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
SERVICE

systemctl daemon-reload
systemctl enable telegram-bot
systemctl start telegram-bot
systemctl status telegram-bot
SETUP
        echo ""
        echo "✅ Done! Bot runs 24/7 with auto-restart"
        ;;
    
    4)
        echo ""
        echo "🐍 PythonAnywhere Deployment"
        echo "============================"
        echo ""
        echo "Step 1: Go to pythonanywhere.com"
        echo "Step 2: Create account"
        echo "Step 3: Upload files in Files tab"
        echo "Step 4: Create virtual environment"
        echo "Step 5: Install requirements"
        echo "Step 6: Create scheduled task or console"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md for details"
        ;;
    
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
