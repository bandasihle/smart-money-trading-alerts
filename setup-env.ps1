# Setup script for environment variables (Windows PowerShell)
# This script helps you safely set up your .env file

Write-Host "🔐 Smart Money Trading Alerts - Environment Setup" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANT: Never commit your .env file to version control!" -ForegroundColor Yellow
Write-Host ""

# Check if .env already exists
if (Test-Path .env) {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
    Write-Host "Note: Make sure to keep sensitive info safe" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "📝 Creating .env file from template..." -ForegroundColor Cyan
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "✅ .env file created from .env.example" -ForegroundColor Green
    } else {
        Write-Host "❌ .env.example not found. Creating basic .env..." -ForegroundColor Red
        @"
# Environment Variables
# Add your sensitive information here

# Pushover Configuration
PUSHOVER_APP_TOKEN=your_token_here
PUSHOVER_USER_KEY=your_user_key_here

# Optional API Keys
# ALPHA_VANTAGE_API_KEY=your_key_here
# TWELVE_DATA_API_KEY=your_key_here
"@ | Out-File .env -Encoding UTF8
        Write-Host "✅ Basic .env file created" -ForegroundColor Green
    }
    Write-Host ""
}

# Check if .env is properly ignored
$gitignorePath = ".gitignore"
if (Test-Path $gitignorePath) {
    $content = Get-Content $gitignorePath
    if ($content -contains ".env") {
        Write-Host "✅ .env is properly listed in .gitignore" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env is NOT in .gitignore - adding it now..." -ForegroundColor Yellow
        Add-Content $gitignorePath "`n.env"
        Write-Host "✅ Added .env to .gitignore" -ForegroundColor Green
    }
} else {
    Write-Host "⚠️  .gitignore not found!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🔧 Next steps:" -ForegroundColor Cyan
Write-Host "1. Open .env file and add your credentials:"
Write-Host "   - PUSHOVER_APP_TOKEN: Get from https://pushover.net/"
Write-Host "   - PUSHOVER_USER_KEY: Get from https://pushover.net/"
Write-Host ""
Write-Host "2. To use environment variables in Python:" -ForegroundColor Cyan
Write-Host "   from dotenv import load_dotenv"
Write-Host "   import os"
Write-Host "   load_dotenv()"
Write-Host "   token = os.getenv('PUSHOVER_APP_TOKEN')"
Write-Host ""
Write-Host "3. For Vercel deployment, add secrets in:" -ForegroundColor Cyan
Write-Host "   Settings → Environment Variables"
Write-Host ""
Write-Host "4. For GitHub CI/CD, add secrets in:" -ForegroundColor Cyan
Write-Host "   Settings → Secrets and variables → Actions"
Write-Host ""
Write-Host "📚 See SECURITY.md for complete documentation" -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
