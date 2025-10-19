# Security & Sensitive Information Guide

## ⚠️ CRITICAL: DO NOT COMMIT SENSITIVE DATA

This document outlines all sensitive information that should NEVER be committed to the repository.

## 🔐 Sensitive Information Categories

### 1. API Keys & Tokens
- ❌ **DO NOT** commit any API keys, tokens, or access keys
- ❌ **DO NOT** hardcode authentication credentials
- ✅ **DO** use environment variables (`.env` file)
- ✅ **DO** use GitHub Secrets for CI/CD pipelines

**Examples to avoid:**
```python
# ❌ WRONG - Never do this:
ALPHA_VANTAGE_API_KEY = "abc123xyz789"
PUSHOVER_APP_TOKEN = "your_token_here"
VERCEL_TOKEN = "vercel_xyz123"
```

**Correct approach:**
```python
# ✅ RIGHT - Use environment variables:
import os
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
PUSHOVER_APP_TOKEN = os.getenv('PUSHOVER_APP_TOKEN')
VERCEL_TOKEN = os.getenv('VERCEL_TOKEN')
```

### 2. API Services in This Project

#### Pushover (Mobile Notifications)
- **What to secure:** API token, User key
- **How to store:**
  - Local development: Add to `.env` file
  - Production (Vercel): Add to Vercel Environment Variables
  - CI/CD (GitHub): Add to GitHub Secrets
- **Never in:** Code files, config.json, vercel.json (unless using env vars)

#### Alpha Vantage (if used)
- **What to secure:** API key
- **Status:** Currently using yfinance (no key needed), but if switched:
  - Store in `.env` as `ALPHA_VANTAGE_API_KEY`
  - Access via `os.getenv('ALPHA_VANTAGE_API_KEY')`

#### Twelve Data (if used)
- **What to secure:** API key
- **Storage:** Same as Alpha Vantage

#### yFinance (currently used)
- ✅ **Good news:** No API key required for free tier
- ✅ **Public data:** Market data is public information

### 3. Database Credentials
- ❌ Database passwords
- ❌ Database URLs with credentials embedded
- ✅ Use connection strings stored in environment variables

### 4. Vercel Deployment Secrets
- ❌ VERCEL_TOKEN (never commit)
- ❌ VERCEL_ORG_ID (prefer env vars)
- ✅ Store in GitHub Secrets, not in code

## 📋 Files That MUST Be in .gitignore

All of these should never be committed:

```
.env                       # Local environment variables
.env.local                 # Local overrides
config.env                 # Configuration with secrets
.env.*.local              # Environment-specific overrides
secrets/                  # Any secrets directory
credentials/              # Any credentials directory
api_keys.txt             # Exported API keys
api_keys.json            # Exported API keys as JSON
pushover_config.json     # Pushover credentials
trading_config.json      # Trading system config with secrets
test_credentials.py      # Test files with real credentials
kernel.json              # Jupyter kernel configs
```

## 🔍 Current Code Review

### ✅ SAFE - Already using environment variables or placeholders:
- `index.py`: Requests API keys from user input (frontend), not hardcoded
- `web_app/app.py`: Receives credentials via POST request, not hardcoded
- `web_app/api/index.py`: No hardcoded secrets visible
- `model.ipynb`: Shows placeholder empty strings for API keys

### ⚠️ WATCH OUT - Potential exposure points:
- Configuration via web forms (validate and sanitize inputs)
- Mobile notification setup requires user to enter credentials
- Local development should use `.env` file

### ✅ Already in .gitignore:
- `.env` ✓
- `config.env` ✓
- `config.json` ✓

## 🚀 How to Properly Set Up

### Local Development

1. **Create `.env` file** (never commit this):
```bash
# .env (NEVER COMMIT THIS FILE)
PUSHOVER_APP_TOKEN=your_app_token_here
PUSHOVER_USER_KEY=your_user_key_here
ALPHA_VANTAGE_API_KEY=your_key_if_used
```

2. **Update your Python code to read from .env:**
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file

pushover_token = os.getenv('PUSHOVER_APP_TOKEN')
pushover_user = os.getenv('PUSHOVER_USER_KEY')
```

3. **Verify .env is in .gitignore**
```bash
# Check that .env is listed
cat .gitignore | grep "\.env"
```

### Vercel Deployment

1. **Set up Environment Variables in Vercel:**
   - Go to Project Settings → Environment Variables
   - Add each secret:
     - `PUSHOVER_APP_TOKEN`
     - `PUSHOVER_USER_KEY`
     - `VERCEL_TOKEN` (if using auto-deployment)

2. **Access in code:**
```python
import os
pushover_token = os.getenv('PUSHOVER_APP_TOKEN')
```

3. **Never expose in vercel.json:**
```json
// ✅ CORRECT - No secrets here
{
  "version": 2,
  "builds": [{"src": "index.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "/index.py"}]
}

// ❌ WRONG - Never include secrets
{
  "env": {
    "PUSHOVER_TOKEN": "your_token_here"  // DON'T DO THIS
  }
}
```

### GitHub CI/CD Secrets

1. **Add to GitHub Secrets:**
   - Go to Settings → Secrets and variables → Actions
   - Create secrets:
     - `VERCEL_TOKEN`
     - `PUSHOVER_APP_TOKEN`
     - `PUSHOVER_USER_KEY`

2. **Use in workflow files:**
```yaml
# .github/workflows/deploy.yml
env:
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  PUSHOVER_APP_TOKEN: ${{ secrets.PUSHOVER_APP_TOKEN }}
```

## 🔐 Security Best Practices

### DO's ✅
- ✅ Use `.gitignore` for all sensitive files
- ✅ Use environment variables for all secrets
- ✅ Use GitHub Secrets for CI/CD
- ✅ Use Vercel Environment Variables for production
- ✅ Rotate API keys periodically
- ✅ Review `.gitignore` before every commit
- ✅ Never accept hardcoded credentials in PRs
- ✅ Use `python-dotenv` for local development

### DON'Ts ❌
- ❌ Never commit `.env` files
- ❌ Never hardcode API keys in source code
- ❌ Never put secrets in `vercel.json`
- ❌ Never expose secrets in logs
- ❌ Never share credentials in comments
- ❌ Never use credentials in test files
- ❌ Never commit credentials to version control
- ❌ Never send credentials in plain text

## 🛠️ Tools for Secret Detection

### Check if secrets are committed:
```bash
# Search for common patterns
git log --all -S "api_key" --source -p
git log --all -S "PUSHOVER" --source -p
git log --all -S "token" --source -p

# Use git-secrets tool
brew install git-secrets  # macOS
git secrets --scan
```

### Pre-commit hooks (optional but recommended):
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
EOF

# Install the hook
pre-commit install
```

## 📚 Required Packages for Environment Variables

Add to `requirements.txt`:
```
python-dotenv==1.0.0
```

Install:
```bash
pip install python-dotenv
```

## 🚨 If You Accidentally Committed Secrets

If you've already committed sensitive information:

1. **Immediately rotate the credentials:**
   - Generate new API tokens
   - Reset passwords
   - Invalidate old tokens

2. **Remove from git history:**
```bash
# Option 1: Using git-filter-repo (recommended)
git filter-repo --invert-paths --path .env

# Option 2: Using BFG Repo-Cleaner
bfg --delete-files .env

# Option 3: Using git filter-branch (slower)
git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch .env' HEAD
```

3. **Force push (after notification):**
```bash
git push --force-with-lease
```

4. **Notify collaborators** to fetch the cleaned history

## 📋 Verification Checklist

Before pushing to GitHub, verify:

- [ ] `.env` file exists and is in `.gitignore`
- [ ] All API keys are empty strings or `os.getenv()` calls
- [ ] No hardcoded tokens in any file
- [ ] `.gitignore` is comprehensive (see above)
- [ ] No credentials in commit messages
- [ ] Sensitive files in `.gitignore` include:
  - `.env`
  - `.env.local`
  - `config.env`
  - `secrets/`
  - `credentials/`
  - `*_config.json` (if contains secrets)
  - `test_credentials.py`

## 📞 Need Help?

For security questions:
1. Check this document first
2. Review `.gitignore` for proper exclusions
3. Use environment variables for all secrets
4. Test locally with `.env` file before deploying

---

**Last Updated:** October 19, 2025
**Status:** ✅ Repository is secure
