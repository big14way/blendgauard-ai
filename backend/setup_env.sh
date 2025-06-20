#!/bin/bash
# BlendGuard Demo Environment Setup Script

echo "🛡️ Setting up BlendGuard Demo Environment..."

# Set environment variables for current session
export DEEPLINK_SECRET="blendguard_hmac_secret_for_demo_protection_links_hackathon_2025"
export TELEGRAM_TOKEN="7837740210:AAHpN4ZdjBVfWU2OM0wm6_5bBdcrJ_Yt3kM"
export FRONTEND_URL="http://localhost:3000"
export DEMO_MODE="true"
export PORT="5001"

echo "✅ Environment variables set for current session:"
echo "  DEEPLINK_SECRET: ${DEEPLINK_SECRET:0:20}..."
echo "  TELEGRAM_TOKEN: ${TELEGRAM_TOKEN:0:15}..."
echo "  FRONTEND_URL: $FRONTEND_URL"
echo "  DEMO_MODE: $DEMO_MODE"
echo "  PORT: $PORT"

echo ""
echo "🚀 You can now run:"
echo "  python3 app.py        # Start the backend API"
echo "  python3 alert_bot.py  # Start the Telegram bot"
echo ""
echo "💡 To make these permanent, add them to your ~/.bashrc or ~/.zshrc" 