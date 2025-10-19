#!/bin/bash
# Setup script for environment variables
# This script helps you safely set up your .env file

set -e

echo "🔐 Smart Money Trading Alerts - Environment Setup"
echo "=================================================="
echo ""
echo "⚠️  IMPORTANT: Never commit your .env file to version control!"
echo ""

# Check if .env already exists
if [ -f .env ]; then
    echo "✅ .env file already exists"
    echo "Opening for editing... (Note: Make sure to keep sensitive info safe)"
    sleep 2
else
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created from .env.example"
    echo ""
fi

# Check if .env is properly ignored
if grep -q "^\.env$" .gitignore 2>/dev/null; then
    echo "✅ .env is properly listed in .gitignore"
else
    echo "⚠️  .env is NOT in .gitignore - adding it now..."
    echo ".env" >> .gitignore
    echo "✅ Added .env to .gitignore"
fi

echo ""
echo "🔧 Next steps:"
echo "1. Edit .env file and add your credentials:"
echo "   - PUSHOVER_APP_TOKEN: Get from https://pushover.net/"
echo "   - PUSHOVER_USER_KEY: Get from https://pushover.net/"
echo ""
echo "2. To use environment variables in Python:"
echo "   from dotenv import load_dotenv"
echo "   import os"
echo "   load_dotenv()"
echo "   token = os.getenv('PUSHOVER_APP_TOKEN')"
echo ""
echo "3. For Vercel deployment, add secrets in:"
echo "   Settings → Environment Variables"
echo ""
echo "4. For GitHub CI/CD, add secrets in:"
echo "   Settings → Secrets and variables → Actions"
echo ""
echo "📚 See SECURITY.md for complete documentation"
echo "✅ Setup complete!"
