# Security & Sensitive Information Guide

## CRITICAL: DO NOT COMMIT SENSITIVE DATA

This document outlines all sensitive information that should NEVER be committed to the repository.

## Sensitive Information Categories

### 1. API Keys & Tokens

DO NOT commit any API keys, tokens, or access keys. DO NOT hardcode authentication credentials.

WRONG - Never do this:
```python
ALPHA_VANTAGE_API_KEY = "abc123xyz789"
PUSHOVER_APP_TOKEN = "your_token_here"
VERCEL_TOKEN = "vercel_xyz123"
```

CORRECT - Use environment variables:
```python
import os
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
PUSHOVER_APP_TOKEN = os.getenv('PUSHOVER_APP_TOKEN')
VERCEL_TOKEN = os.getenv('VERCEL_TOKEN')
```

### 2. API Services in This Project

#### Pushover (Mobile Notifications)
- Secure: API token, User key
- Local: Add to `.env` file
- Production (Vercel): Add to Vercel Environment Variables
- CI/CD (GitHub): Add to GitHub Secrets
- Never in: Code files, config.json, vercel.json

#### Alpha Vantage (if used)
- Secure: API key
- Store in `.env` as `ALPHA_VANTAGE_API_KEY`
- Access via `os.getenv('ALPHA_VANTAGE_API_KEY')`

#### Twelve Data (if used)
- Secure: API key
- Same storage as Alpha Vantage

#### yFinance (currently used)
- No API key required for free tier
- Market data is public information

### 3. Database Credentials
- Never commit database passwords
- Never commit database URLs with credentials embedded
- Use connection strings stored in environment variables

### 4. Vercel Deployment Secrets
- Never commit VERCEL_TOKEN
- Never commit VERCEL_ORG_ID directly
- Store in GitHub Secrets, not in code

## Files That MUST Be in .gitignore

```
.env                       Local environment variables
.env.local                 Local overrides
config.env                 Configuration with secrets
.env.*.local              Environment-specific overrides
secrets/                  Any secrets directory
credentials/              Any credentials directory
api_keys.txt             Exported API keys
api_keys.json            Exported API keys as JSON
pushover_config.json     Pushover credentials
trading_config.json      Trading system config with secrets
test_credentials.py      Test files with real credentials
kernel.json              Jupyter kernel configs
```

## Current Code Review

### SAFE - Already using environment variables or placeholders:
- index.py: Requests API keys from user input (frontend), not hardcoded
- web_app/app.py: Receives credentials via POST request, not hardcoded
- web_app/api/index.py: No hardcoded secrets visible
- model.ipynb: Shows placeholder empty strings for API keys

### WATCH OUT - Potential exposure points:
- Configuration via web forms (validate and sanitize inputs)
- Mobile notification setup requires user to enter credentials
- Local development should use `.env` file

### Already in .gitignore:
- .env
- config.env
- config.json

## Setup Instructions

### Local Development

1. Create `.env` file (never commit this):
```bash
PUSHOVER_APP_TOKEN=your_app_token_here
PUSHOVER_USER_KEY=your_user_key_here
ALPHA_VANTAGE_API_KEY=your_key_if_used
```

2. Update Python code to read from .env:
```python
from dotenv import load_dotenv
import os

load_dotenv()

pushover_token = os.getenv('PUSHOVER_APP_TOKEN')
pushover_user = os.getenv('PUSHOVER_USER_KEY')
```

3. Verify .env is in .gitignore:
```bash
cat .gitignore | grep "\.env"
```

### Vercel Deployment

1. Set up Environment Variables in Vercel:
   - Go to Project Settings → Environment Variables
   - Add each secret:
     - PUSHOVER_APP_TOKEN
     - PUSHOVER_USER_KEY
     - VERCEL_TOKEN (if using auto-deployment)

2. Access in code:
```python
import os
pushover_token = os.getenv('PUSHOVER_APP_TOKEN')
```

3. Never expose in vercel.json:
```json
{
  "version": 2,
  "builds": [{"src": "index.py", "use": "@vercel/python"}],
  "routes": [{"src": "/(.*)", "dest": "/index.py"}]
}
```

### GitHub CI/CD Secrets

1. Add to GitHub Secrets:
   - Go to Settings → Secrets and variables → Actions
   - Create secrets:
     - VERCEL_TOKEN
     - PUSHOVER_APP_TOKEN
     - PUSHOVER_USER_KEY

2. Use in workflow files:
```yaml
env:
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  PUSHOVER_APP_TOKEN: ${{ secrets.PUSHOVER_APP_TOKEN }}
```

## Security Best Practices

### DO's
- Use `.gitignore` for all sensitive files
- Use environment variables for all secrets
- Use GitHub Secrets for CI/CD
- Use Vercel Environment Variables for production
- Rotate API keys periodically
- Review `.gitignore` before every commit
- Never accept hardcoded credentials in PRs
- Use `python-dotenv` for local development

### DON'Ts
- Never commit `.env` files
- Never hardcode API keys in source code
- Never put secrets in `vercel.json`
- Never expose secrets in logs
- Never share credentials in comments
- Never commit credentials to version control
- Never send credentials in plain text
- Never use credentials in test files

## Tools for Secret Detection

### Check if secrets are committed:
```bash
git log --all -S "api_key" --source -p
git log --all -S "PUSHOVER" --source -p
git log --all -S "token" --source -p
```

### Use git-secrets tool:
```bash
brew install git-secrets
git secrets --scan
```

## If You Accidentally Committed Secrets

If sensitive information was already committed:

1. Immediately rotate the credentials:
   - Generate new API tokens
   - Reset passwords
   - Invalidate old tokens

2. Remove from git history:
```bash
git filter-repo --invert-paths --path .env
```

3. Force push (after notification):
```bash
git push --force-with-lease
```

4. Notify collaborators to fetch the cleaned history

## Verification Checklist

Before pushing to GitHub, verify:

- [ ] `.env` file exists and is in `.gitignore`
- [ ] All API keys are empty strings or `os.getenv()` calls
- [ ] No hardcoded tokens in any file
- [ ] `.gitignore` is comprehensive
- [ ] No credentials in commit messages
- [ ] Sensitive files in `.gitignore` include:
  - .env
  - .env.local
  - config.env
  - secrets/
  - credentials/
  - *_config.json
  - test_credentials.py

## Required Packages

Add to `requirements.txt`:
```
python-dotenv==1.0.0
```

Install:
```bash
pip install python-dotenv
```

## Setup Steps

### For macOS/Linux:
```bash
cp .env.example .env
# Edit .env and add your credentials
source venv/bin/activate
pip install -r requirements.txt
```

### For Windows:
```bash
copy .env.example .env
# Edit .env and add your credentials
venv\Scripts\activate
pip install -r requirements.txt
```
