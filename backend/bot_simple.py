#!/usr/bin/env python3
"""
Simplified BlendGuard Telegram Bot
Fixed version without event loop issues
"""
import os
import logging
import asyncio
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import TELEGRAM_TOKEN
from alert_bot import get_user_positions, get_contract_info, generate_deeplink

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    if not update.message:
        return
        
    welcome_message = """
🛡️ **Welcome to BlendGuard!**

I'm your personal Stellar lending protection assistant. I monitor your positions and help protect them from liquidation.

**Available Commands:**
• `/status` - Check your position health
• `/contract` - View BlendGuard contract info

Stay safe! 🚀
"""
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def handle_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - show user's lending positions and risks"""
    if not update.message or not update.message.from_user:
        return
        
    user_id = str(update.message.from_user.id)
    positions = get_user_positions(user_id)
    
    if not positions:
        no_positions_message = """
📊 **Position Status**

No active lending positions found.

Connect your wallet to start using Blend lending markets!
"""
        await update.message.reply_text(no_positions_message, parse_mode="Markdown")
        return
    
    status_message = "📊 **Your Lending Positions**\n\n"
    
    keyboard = []
    for position in positions:
        risk_emoji = "🔴" if position['risk_score'] > 0.8 else "🟡" if position['risk_score'] > 0.6 else "🟢"
        status_message += f"{risk_emoji} **{position['asset']}**: ${position['amount']:,}\n"
        status_message += f"   Risk: {position['risk_score']:.0%} | Health: {position['health_factor']:.2f}\n\n"
        
        if position['risk_score'] > 0.7:  # High risk positions
            keyboard.append([InlineKeyboardButton(
                f"🛡️ Activate Protection - {position['asset']}", 
                callback_data=f"protect_{position['id']}"
            )])
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await update.message.reply_text(status_message, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_contract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /contract command - show contract information"""
    if not update.message:
        return
        
    contract_info = get_contract_info()
    contract_message = f"""
🔗 **BlendGuard Contract Info**

**SafetyVault Contract:**
`{contract_info['contract_id']}`

**Network:** {contract_info['network']}
**Version:** {contract_info['version']}

This contract protects your lending positions through automated safety actions.
"""
    await update.message.reply_text(contract_message, parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries from inline keyboards"""
    query = update.callback_query
    if not query or not query.from_user:
        return
        
    await query.answer()
    
    try:
        if query.data and query.data.startswith('protect_'):
            position_id = query.data.split('_')[1]
            user_id = str(query.from_user.id)
            
            # Generate secure deeplink for frontend protection flow
            deeplink = generate_deeplink(position_id, user_id)
            
            keyboard = [[InlineKeyboardButton("🔄 Open Protection App", url=deeplink)]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            protection_message = f"""
🛡️ **Protection Activated!**

Click the button below to open the BlendGuard protection interface and secure your position.

Your protection link is secured with HMAC authentication for maximum safety.
"""
            
            await query.edit_message_text(
                text=protection_message,
                parse_mode="Markdown", 
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")

def main():
    """Main function to run the bot"""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN not set")
        return
    
    logger.info("Starting BlendGuard Bot...")
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", handle_start))
    application.add_handler(CommandHandler("status", handle_status))
    application.add_handler(CommandHandler("contract", handle_contract))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    logger.info("BlendGuard Bot started successfully!")
    logger.info("Send /start to the bot to begin")
    
    # Run the bot
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main() 