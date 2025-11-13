# 🚀 Streamlined Workflow: Edit → Deploy → Test → Repeat

**Fast cycle for continuous refinement without local testing**

---

## ⚡ The Workflow (3 Simple Steps)

### Step 1: Edit Code
Edit `main_cloud.py` in VS Code, then save.

### Step 2: Deploy to GCF
Run one command in terminal:
```bash
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"
```

### Step 3: Test on Telegram
Send a message to your bot and verify the response.

### Step 4: Repeat
Back to Step 1 if needed.

---

## 📝 Quick Edit Locations

### Change Bot System Prompt
**File**: `main_cloud.py`  
**Lines**: 28-37

```python
SYSTEM_PROMPT = """You are an AI assistant.

Your guidelines:
- Respond in simple terms, short and straight to the point
- No fluff
- Structure long responses into paragraphs of 30 words
- For every response translate into simple iban sarawak language
- For every prompt in other languages, translate it and respond in english"""
```

Just edit the prompt text and save. Deploy to test.

### Add New Dependencies
**File**: `requirements_cloud.txt`

```
pyTelegramBotAPI==4.29.1
google-genai>=0.3.0
functions-framework>=3.0.0
# Add new packages here
```

Update file, then deploy.

### Change Bot Logic
**File**: `main_cloud.py`  
**Function**: `get_gemini_response()` (lines 44-80)

Modify the function to change how responses are generated, then deploy.

---

## 🔧 One-Command Deploy

Save this as a shortcut in your terminal:

```bash
# Paste this into your terminal (or add to ~/.zshrc for permanent alias)
alias deploy-bot='./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"'
```

Then just type:
```bash
deploy-bot
```

---

## 📊 Deployment Timeline

| Step | Time | Action |
|------|------|--------|
| Edit code | 1-5 min | Modify `main_cloud.py` |
| Deploy | 2-3 min | Run deploy script (auto-builds & deploys) |
| Test | 1-2 min | Send message in Telegram, verify response |
| **Total** | **5-10 min** | Ready for next iteration |

---

## ✅ Deployment Checklist (Quick Version)

Before you run the deploy command:
- [ ] Saved `main_cloud.py` changes
- [ ] Updated `requirements_cloud.txt` if you added packages
- [ ] Have TG_KEY and GEM_KEY files in project root

That's it! Deploy.

---

## 🎯 Common Edits & Deploy Patterns

### Pattern 1: Tweak System Prompt
```
1. Edit main_cloud.py lines 28-37
2. Run: ./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"
3. Wait 2-3 min
4. Test in Telegram
5. Repeat
```

### Pattern 2: Add New Package
```
1. Add package name to requirements_cloud.txt
2. Run deploy script (same as above)
3. Deploy will fail if package has issues (you'll see error)
4. Fix and redeploy
```

### Pattern 3: Change Response Logic
```
1. Edit main_cloud.py get_gemini_response() function
2. Deploy
3. Test
4. If broken, fix and redeploy
```

---

## 📋 Essential Commands

### Deploy
```bash
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"
```

### View Live Logs (watch for errors)
```bash
source /opt/homebrew/share/google-cloud-sdk/path.zsh.inc
gcloud functions logs read telegram_webhook --region asia-southeast1 --follow
```

### Quick Status Check
```bash
gcloud functions describe telegram_webhook --region asia-southeast1 | grep state
```

### Delete Function (start over)
```bash
gcloud functions delete telegram_webhook --region asia-southeast1
```

---

## 🧪 Testing on Telegram

After deployment:

1. **Open Telegram**
2. **Find your bot**
3. **Send message**: "Hello"
4. **Expected**: AI response (takes 1-5 seconds)

If no response:
- Wait 30 seconds (function might be cold-starting)
- Check logs: `gcloud functions logs read telegram_webhook --region asia-southeast1 --limit 20`
- Redeploy if needed

---

## ⚠️ Common Issues & Fixes

### "Deployment failed"
1. Check syntax: `python -m py_compile main_cloud.py`
2. Check requirements: `pip install -r requirements_cloud.txt`
3. View error logs: `gcloud functions logs read telegram_webhook --region asia-southeast1 --limit 50`

### "Bot not responding in Telegram"
1. Wait 30 seconds (cold start)
2. Check logs for errors
3. Verify webhook is still set (deployment resets it automatically)

### "Package not found error"
1. Check package name spelling in `requirements_cloud.txt`
2. Make sure it's a valid PyPI package
3. Redeploy

---

## 🎓 Example Refinement Cycle

### Iteration 1: Change Tone
```
Edit main_cloud.py:
SYSTEM_PROMPT = """You are a casual, friendly AI..."""

Deploy: ./deploy_cloud.sh ...
Test: "Hello" → Response is now casual
Good? Keep it. Bad? Edit again.
```

### Iteration 2: Add Spanish Support
```
Edit main_cloud.py SYSTEM_PROMPT:
- Add "Respond in Spanish when asked"

Deploy: ./deploy_cloud.sh ...
Test: "Hola" → Response in Spanish
Good? Keep it. Need tweaks? Edit again.
```

### Iteration 3: Add New Package
```
Edit requirements_cloud.txt:
requests==2.31.0

Edit main_cloud.py:
import requests
# Add new functionality

Deploy: ./deploy_cloud.sh ...
Test: Verify new feature works
```

---

## 📱 Quick Telegram Test Checklist

After each deployment, send these test messages:

- [ ] "Hello" → Should get response
- [ ] "What is 2+2?" → Should get answer
- [ ] "Tell me a joke" → Should get joke
- [ ] Empty message → Should handle gracefully
- [ ] Long message → Should split if >4096 chars

---

## 🚀 Pro Tips

1. **Use the alias**: Add to `~/.zshrc`:
   ```bash
   alias deploy-bot='./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"'
   ```
   Then just type: `deploy-bot`

2. **Watch logs while testing**: 
   In one terminal: `gcloud functions logs read telegram_webhook --region asia-southeast1 --follow`
   In another: Test in Telegram
   See real-time logs!

3. **Version your changes**: Add comments in code when making refinements
   ```python
   # v1: Initial prompt
   # v2: Added Spanish support
   # v3: Fixed tone to be more casual
   SYSTEM_PROMPT = """..."""
   ```

4. **Keep TG_KEY and GEM_KEY safe**: Never commit to git (.gitignore already protects them)

5. **Fast iteration**: 5-10 min per cycle means you can test many ideas quickly

---

## 📊 Your Current Setup

| Component | Status | Details |
|-----------|--------|---------|
| GCF Function | ✅ Active | Running in Singapore (asia-southeast1) |
| Code | ✅ Ready | main_cloud.py with webhook handler |
| Dependencies | ✅ Ready | requirements_cloud.txt configured |
| Deploy Script | ✅ Ready | deploy_cloud.sh automated |
| Credentials | ✅ Ready | TG_KEY and GEM_KEY in project root |
| Workflow | ✅ Ready | Edit → Deploy → Test cycle |

---

## 🎯 Ready to Start Refining?

You're all set! Here's your workflow:

```bash
# 1. Edit main_cloud.py in VS Code
# 2. Save
# 3. Run this:
./deploy_cloud.sh gen-lang-client-0715057599 asia-southeast1 "$(cat TG_KEY)" "$(cat GEM_KEY)"

# 4. Wait for "✅ Cloud Function deployed successfully!"
# 5. Test in Telegram
# 6. Repeat!
```

**That's it. You're ready to iterate! 🚀**

---

## 📞 Quick Reference

**To edit and deploy:**
1. `main_cloud.py` → System prompt (lines 28-37)
2. `main_cloud.py` → Response logic (lines 44-80)
3. `requirements_cloud.txt` → Add packages
4. Run deploy script
5. Test on Telegram
6. Repeat

**When things go wrong:**
- Check logs: `gcloud functions logs read telegram_webhook --region asia-southeast1 --limit 50`
- Verify syntax: `python -m py_compile main_cloud.py`
- Redeploy: Same deploy command

**Key files you'll work with:**
- `main_cloud.py` - Your bot code (edit here)
- `requirements_cloud.txt` - Dependencies (edit here)
- `deploy_cloud.sh` - Deployment (just run this)

---

**Happy refining! Each cycle is just 5-10 minutes! 🎉**
