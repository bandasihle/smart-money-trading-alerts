# Trading Alert System - Manual Vercel Deployment Script (Windows)
# Run this script to deploy your trading system to Vercel

Write-Host "🚀 Deploying Smart Money Trading Alert System to Vercel..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if we're in the right directory
if (!(Test-Path "vercel.json")) {
    Write-Host "❌ Error: Please run this script from the web_app directory" -ForegroundColor Red
    Write-Host "   cd web_app && ./DEPLOY_MANUAL.ps1" -ForegroundColor Yellow
    exit 1
}

# Check if Node.js is installed
try {
    node --version | Out-Null
} catch {
    Write-Host "❌ Error: Node.js is required but not installed" -ForegroundColor Red
    Write-Host "   Please install Node.js from https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Check if Vercel CLI is installed
try {
    vercel --version | Out-Null
} catch {
    Write-Host "📦 Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

# Deploy to Vercel
Write-Host "🔄 Deploying to Vercel..." -ForegroundColor Blue
vercel --prod

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Your trading alert system is now live 24/7!" -ForegroundColor Cyan
Write-Host "🌐 Visit your dashboard at the URL shown above" -ForegroundColor Cyan
Write-Host "📧 Don't forget to configure your Pushover API keys in Vercel dashboard" -ForegroundColor Yellow
Write-Host ""
Write-Host "🔧 Next steps:" -ForegroundColor Magenta
Write-Host "   1. Go to vercel.com dashboard" -ForegroundColor White
Write-Host "   2. Find your project settings" -ForegroundColor White
Write-Host "   3. Add environment variables:" -ForegroundColor White
Write-Host "      - PUSHOVER_USER_KEY=your_user_key" -ForegroundColor Gray
Write-Host "      - PUSHOVER_API_TOKEN=your_api_token" -ForegroundColor Gray
Write-Host "   4. Test your live system!" -ForegroundColor White