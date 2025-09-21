#!/bin/bash

# Trading Alert System - Manual Vercel Deployment Script
# Run this script to deploy your trading system to Vercel

echo "🚀 Deploying Smart Money Trading Alert System to Vercel..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: Please run this script from the web_app directory"
    echo "   cd web_app && bash DEPLOY_MANUAL.sh"
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Deploy to Vercel
echo "🔄 Deploying to Vercel..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📱 Your trading alert system is now live 24/7!"
echo "🌐 Visit your dashboard at the URL shown above"
echo "📧 Don't forget to configure your Pushover API keys in Vercel dashboard"
echo ""
echo "🔧 Next steps:"
echo "   1. Go to vercel.com dashboard"
echo "   2. Find your project settings"
echo "   3. Add environment variables:"
echo "      - PUSHOVER_USER_KEY=your_user_key"
echo "      - PUSHOVER_API_TOKEN=your_api_token"
echo "   4. Test your live system!"