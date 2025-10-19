# 🔐 Security Setup Guide

This project has been hardened for production use. Follow these steps to ensure your setup is secure.

## Quick Start (Choose One)

### Option 1: Automated Setup (Recommended)

**Windows (PowerShell):**
```powershell
.\setup-env.ps1
```

**macOS/Linux (Bash):**
```bash
bash setup-env.sh
```

### Option 2: Manual Setup

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your credentials:**
   ```bash
   # Open .env and add:
   PUSHOVER_APP_TOKEN=your_token_here
   PUSHOVER_USER_KEY=your_user_key_here
   ```

3. **Install python-dotenv:**
   ```bash
   pip install python-dotenv
   ```

## 🔐 Get Your Credentials

### Pushover (Mobile Notifications)
1. Visit https://pushover.net/
2. Download the mobile app
3. Get your API token and User key
4. Add them to `.env` file

## 📚 Documentation

- **[SECURITY.md](./SECURITY.md)** - Complete security guide
- **[SECURITY_AUDIT.md](./SECURITY_AUDIT.md)** - Full audit report
- **[.env.example](./.env.example)** - Environment variables template

## ✅ Verification

Verify your setup:

```bash
# Check .env is ignored
cat .gitignore | grep -E "^\.env"

# Verify no secrets in code
grep -r "api_key\s*=" . --include="*.py" 2>/dev/null || echo "✅ No hardcoded keys"

# Verify .env exists
test -f .env && echo "✅ .env exists" || echo "❌ .env missing"
```

## 🚀 Deploy Safely

### To Vercel
1. Add Environment Variables in Vercel Settings
2. Variables needed: `PUSHOVER_APP_TOKEN`, `PUSHOVER_USER_KEY`
3. Deploy - Vercel handles environment variables automatically

### To GitHub
- Never commit `.env` file (it's in `.gitignore`)
- Use GitHub Secrets for CI/CD

## 🚨 Important Reminders

- ⚠️ **NEVER** commit your `.env` file
- ⚠️ **NEVER** hardcode API keys in source code
- ⚠️ **ALWAYS** use environment variables for secrets
- ⚠️ **ALWAYS** verify `.env` is in `.gitignore`

## ❓ Need Help?

1. Check `SECURITY.md` for detailed information
2. Review `SECURITY_AUDIT.md` for audit findings
3. See `.env.example` for configuration template

---

**Last Updated:** October 19, 2025  
**Status:** ✅ Repository is secure and ready for production
