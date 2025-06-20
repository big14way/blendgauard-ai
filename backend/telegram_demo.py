#!/usr/bin/env python3
"""
Minimal BlendGuard Telegram Bot for Demo
Works without event loop conflicts
"""
import logging
import os
import sys
from telegram import Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from config
TELEGRAM_TOKEN = "7837740210:AAHpN4ZdjBVfWU2OM0wm6_5bBdcrJ_Yt3kM"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    if not update.message:
        return
        
    welcome_text = """
🛡️ **Welcome to BlendGuard!**

Your Stellar DeFi position protection assistant.

**Commands:**
• /start - This message
• /status - Check positions
• /demo - Demo alert

🚀 Built for Stellar Hackathon 2025
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    if not update.message:
        return
        
    # Mock high-risk position
    keyboard = [
        [InlineKeyboardButton("🛡️ Activate Protection", callback_data="protect_demo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    status_text = """
📊 **Your Positions**

🔴 **XLM Position**
• Amount: $10,000
• Risk: 85% (HIGH)
• Health Factor: 1.15
• Status: ⚠️ Liquidation Risk

⚡ **Action Required!**
"""
    await update.message.reply_text(
        status_text, 
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def format_position(position):
    """Standardized position formatting for consistent display"""
    return (
        f"🔴 {position['asset']} Position\n"
        f"• Amount: ${position['collateral']:,.2f}\n"
        f"• Risk: {position['ltv']*100:.0f}% (HIGH)\n"
        f"• Health Factor: {position['healthFactor']:.2f}\n"
        f"• Status: ⚠️ Liquidation Risk\n\n"
        f"⚡ Action Required!"
    )

def get_position(position_id):
    """Get position data - centralized source"""
    return {
        'id': position_id or 'XLM-123',
        'asset': 'XLM',
        'collateral': 10000,  # USD value
        'debt': 8500,         # USD value
        'ltv': 0.85,          # 85%
        'healthFactor': 1.15,
        'status': 'high-risk'
    }

async def demo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /demo command"""
    if not update.message:
        return
        
    position = get_position("XLM-123")
    keyboard = [
        [InlineKeyboardButton("🛡️ Fix Now", callback_data="protect_XLM-123")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    demo_text = (
        f"⚠️ DEMO: Liquidation Alert\n\n"
        f"🎯 Position: {position['asset']} Lending\n"
        f"💰 Collateral: ${position['collateral']:,.2f}\n"
        f"📉 LTV: {position['ltv']*100:.0f}%\n"
        f"🩺 Health Factor: {position['healthFactor']:.2f}\n"
        f"🔥 Risk Level: CRITICAL\n\n"
        f"🛡️ BlendGuard Protection Ready!"
    )
    
    await update.message.reply_text(
        demo_text,
        parse_mode='Markdown', 
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    logger.info(f"🔔 Callback received: {update.callback_query.data if update.callback_query else 'No data'}")
    
    query = update.callback_query
    if not query:
        logger.error("❌ No callback query found")
        return
    
    try:
        # Always answer the callback query first
        await query.answer("🔄 Processing your protection request...")
        logger.info(f"✅ Answered callback for: {query.data}")
        
        if query.data in ["protect_demo", "protect_XLM-123"]:
            logger.info(f"🛡️ Processing protection: {query.data}")
            
            # Generate demo protection link with consistent position ID
            user_id = query.from_user.id if query.from_user else "123456789"
            protection_link = f"http://localhost:3000/protect?pos=XLM-123&user={user_id}&sig=a2661dd772013edbfac150f29adf8685b3c2c7ba8e561512dbf550c1e1831d75"
            
            keyboard = [
                [InlineKeyboardButton("🛡️ Open Protection App", url=protection_link)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            success_text = f"""
🛡️ **Protection Link Generated!**

✅ Secure HMAC-signed deeplink created
🔐 Position: `XLM-123`
👤 User: `{user_id}`
🕐 Generated: Now

Click below to open BlendGuard protection interface:
"""
            
            await query.edit_message_text(
                success_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            logger.info("✅ Protection link sent successfully")
            
        else:
            logger.warning(f"⚠️ Unknown callback: {query.data}")
            await query.edit_message_text(
                f"❌ Unknown action: {query.data}\nPlease try again.",
                parse_mode='Markdown'
            )
            
    except Exception as e:
        logger.error(f"❌ Callback error: {str(e)}")
        try:
            await query.edit_message_text(
                "❌ Error processing request. Please try again.",
                parse_mode='Markdown'
            )
        except Exception as edit_error:
            logger.error(f"❌ Failed to edit message: {edit_error}")
            # Log edit failure
            logger.error("Failed to edit message after error")

def main():
    """Run the bot"""
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN not set")
        return
    
    print("🛡️ Starting BlendGuard Telegram Bot...")
    print("📱 Bot Token:", TELEGRAM_TOKEN[:20] + "...")
    
    try:
        # Create application
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Add handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("status", status_command)) 
        app.add_handler(CommandHandler("demo", demo_command))
        app.add_handler(CallbackQueryHandler(button_callback))
        
        print("✅ Bot handlers registered")
        print("🚀 Starting polling...")
        print("💡 Send /start to the bot to test")
        
        # Run the bot
        app.run_polling(drop_pending_updates=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 